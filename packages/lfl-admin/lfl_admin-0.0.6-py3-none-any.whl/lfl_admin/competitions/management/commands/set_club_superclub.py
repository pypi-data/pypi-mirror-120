import logging

from django.core.management import BaseCommand
from tqdm import tqdm

from lfl_admin.competitions.models.clubs import Clubs

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        query = Clubs.objects.filter( parent=None )
        pbar = tqdm( total=query.count() )
        for club in query :
            if club.old_superclub_id is not None :
                club.parent = Clubs.objects.getOr( old_ids__overlap=[ club.old_superclub_id ] , alternative=Clubs.unknown )
                club.save()
            pbar.update()
