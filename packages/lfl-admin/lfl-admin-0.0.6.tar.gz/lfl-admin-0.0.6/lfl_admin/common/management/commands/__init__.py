from django.db import connection , transaction

from lfl_admin.common.models.all_tables import All_tables


def update_img_refs(old_id, new_id):
    with transaction.atomic() :
        with connection.cursor() as cursor :
            for table in All_tables.objects.filter( table_name__endswith='_images' ).exclude( table_name__in=[ 'common_site_lfl_images' , 'isc_common_images' ] ).order_by( 'table_name' ) :

                cursor.execute( f'update {table.table_name} set image_id=%s where image_id=%s',[new_id, old_id] )

            cursor.execute( f'delete from isc_common_images where id=%s',[old_id] )

def delete_img_refs(old_id):
    with transaction.atomic():
        with connection.cursor() as cursor :
            for table in All_tables.objects.filter( table_name__endswith='_images' ).exclude( table_name__in=[ 'common_site_lfl_images' , 'isc_common_images' ] ).order_by( 'table_name' ) :
                cursor.execute( f'delete from {table.table_name} where image_id=%s',[old_id] )

            cursor.execute( f'delete from isc_common_images where id=%s',[old_id] )
