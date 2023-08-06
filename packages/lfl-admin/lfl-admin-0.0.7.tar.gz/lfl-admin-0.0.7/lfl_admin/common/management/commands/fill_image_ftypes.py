import logging

from django.core.management import BaseCommand
from django.db import transaction , connection

from isc_common.models.images import Images
from lfl_admin.common.models.all_tables import All_tables

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Установка правильных типов картиноц"

    def handle( self , *args , **options ) :
        i = 1
        with transaction.atomic() :
            for table in All_tables.objects.filter( table_name__endswith='_images' ).exclude( table_name__in=[ 'common_site_lfl_images' , 'isc_common_images' ] ).order_by( 'table_name' ) :
                print( table.table_name )
                with connection.cursor() as cursor :
                    cursor.execute( f'select id, image_id from {table.table_name}' )
                    rows = cursor.fetchall()
                    for row in rows :
                        id , image_id = row
                        cursor.execute( f'select image_type_id from isc_common_images where id = %s', [image_id] )
                        image_type_rows = cursor.fetchall()
                        for image_type_row in image_type_rows:
                            image_type_id, = image_type_row

                            sql_str = f'update {table.table_name} set type_id = %s where id=%s'
                            cursor.execute( sql_str , [ image_type_id , id ] )
                            print( f'# {i}  {table.table_name}  {[ image_type_id , id ]}' )
                            i += 1
