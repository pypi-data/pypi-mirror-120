import logging

from django.db.models import SmallIntegerField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import Model_withOldId, AuditModel, AuditQuerySet, AuditManager

from lfl_admin.competitions.models.calendar import Calendar
from lfl_admin.competitions.models.match_stat_types import Match_stat_types

logger = logging.getLogger(__name__)


class Match_statsQuerySet(AuditQuerySet):
    pass


class Match_statsManager(AuditManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'away_value': record.away_value,
            'deliting': record.deliting,
            'editing': record.editing,
            'home_value': record.home_value,
            'id': record.id,
            # 'match__name': record.match.name,
            'match_id': record.match.id,
            'type__name': record.type.name,
            'type_id': record.type.id,
        }
        return res

    def get_queryset(self):
        return Match_statsQuerySet(self.model, using=self._db)


class Match_stats(AuditModel, Model_withOldId):
    away_value = SmallIntegerField(null=True, blank=True)
    home_value = SmallIntegerField(null=True, blank=True)
    match = ForeignKeyCascade(Calendar)
    type = ForeignKeyProtect(Match_stat_types)

    objects = Match_statsManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Статистика матча'
