import logging

from django.core.management import BaseCommand

from lfl_admin.common.models.all_tables import All_tables
from lfl_admin.competitions.models.tournaments import Tournaments , TournamentsManager

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        for table in All_tables.objects.filter( table_name__endswith='_images' ).exclude( table_name__in=[ 'common_site_lfl_images' , 'isc_common_images' ] ).order_by( 'table_name' ) :
            print(table.table_name)
