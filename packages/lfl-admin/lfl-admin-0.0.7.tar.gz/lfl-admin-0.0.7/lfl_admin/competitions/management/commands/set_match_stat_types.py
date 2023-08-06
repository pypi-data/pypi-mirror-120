import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.match_stat_types import Match_stat_types
from lfl_admin.competitions.models.match_stats import Match_stats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle(self, *args, **options):
        with transaction.atomic():
            for match_stat in Match_stats.objects.values('stat_key', 'stat_title').distinct():
                type, _ = Match_stat_types.objects.get_or_create(code=match_stat.get('stat_key'), name=match_stat.get('stat_title'))
                Match_stats.objects.filter(stat_key=match_stat.get('stat_key'), stat_title=match_stat.get('stat_title')).update(type=type)
