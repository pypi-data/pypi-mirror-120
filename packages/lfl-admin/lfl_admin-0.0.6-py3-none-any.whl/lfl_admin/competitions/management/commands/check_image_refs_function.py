import logging

from django.core.management import BaseCommand
from django.db import transaction , connection

from lfl_admin.common.models.all_tables import All_tables

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    # def add_arguments( self , parser ) :
    #     parser.add_argument( '--model' , type=str )

    def handle( self , *args , **options ) :
        params = dict(
            tournaments=[ 'logo' , 'scheme' ] ,
            divisions=[ 'scheme' ]
        )

        with transaction.atomic() :

            with connection.cursor() as cursor :
                for table in All_tables.objects.filter( table_name__endswith='_images' ).exclude( table_name__in=[ 'common_site_lfl_images' , 'isc_common_images' ] ).order_by( 'table_name' ) :
                    cursor.execute( f'''select t.id, t.code, t.keyimage
                                        from isc_common_image_types t
                                        where id in (select distinct icit.id
                                                     from {table.table_name} cti
                                                              join isc_common_image_types icit on cti.type_id = icit.id)''' )

                    rindex = table.table_name.rfind( '_' )
                    index = table.table_name.find( '_' )
                    model = table.table_name[ index + 1 : rindex ]

                    for keyimage in params.get( model , [ ] ) :
                        code = model
                        rows = cursor.fetchall()
                        for row in rows :
                            id , _code , _keyimage = row

                            cursor.execute( f"select count(*) from isc_common_image_types where code = %s and keyimage = %s" , [ code , keyimage ] )
                            cnt , = cursor.fetchone()

                            if cnt == 0 :
                                cursor.execute( f'''insert into isc_common_image_types (deleted_at, editing, deliting, lastmodified, code, name, description, parent_id, height, width, keyimage)
                                                    select deleted_at, editing, deliting, lastmodified, %s, name, description, parent_id, height, width, %s from isc_common_image_types where id=%s 
                                                    RETURNING id ''' , [ code , keyimage , id ] )

                                _id , = cursor.fetchone()
                                cursor.execute( f'''update {table.table_name} set type_id = %s where type_id = %s;''' , [ _id , id ] )
