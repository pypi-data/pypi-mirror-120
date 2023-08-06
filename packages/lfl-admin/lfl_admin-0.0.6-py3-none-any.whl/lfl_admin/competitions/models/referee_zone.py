import logging

from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet, Model_withOldId

from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.competitions.models.referees import Referees

logger = logging.getLogger(__name__)


class Referee_zoneQuerySet(AuditQuerySet):
    pass


class Referee_zoneManager(AuditManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'deliting': record.deliting,
            'editing': record.editing,
            'id': record.id,
            'league__name': record.league.name,
            'league_id': record.league.id,
            'referee__name' : record.league.name ,
            'referee_id' : record.referee.id ,
            'region__name': record.league.region.name,
            'region_id': record.league.region.id,
        }
        return res

    def get_queryset(self):
        return Referee_zoneQuerySet(self.model, using=self._db)


class Referee_zone(AuditModel, Model_withOldId):
    league = ForeignKeyProtect(Leagues)
    referee = ForeignKeyCascade(Referees)

    objects = Referee_zoneManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Главные судьи в матчах'
        unique_together = (('referee', 'league'),)
