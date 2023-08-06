import logging
import uuid

from django.core.management import BaseCommand
from isc_common.number import ToStr

from lfl_admin.competitions.models.tournaments import Tournaments

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        logger.debug( self.help )

        # print( Tournaments.get_urls_data( code='logo' , id=12577 ))
        print(ToStr(uuid.uuid4()))
