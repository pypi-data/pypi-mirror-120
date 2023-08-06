import logging

from django.core.management import BaseCommand

from lfl_admin.inventory.models.clothes_clubs import Clothes_clubs

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        Clothes_clubs.objects.update_or_create( club=86244 , clothes_type='shirts' , code='shirts' , name='Основной цвет маек' , clothes_context='жёлтый' )
        print( Clothes_clubs.objects.get_cloth_context( club=86244 , clothes_type='shirts' , code='shirts' ) )
