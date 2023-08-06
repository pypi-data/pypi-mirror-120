import logging

from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet, Model_withOldId

from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.competitions.models.referees import Referees
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger(__name__)


class Referee_zone_viewQuerySet(AuditQuerySet):
    pass


class Referee_zone_viewManager(AuditManager):

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
            'region__name': record.region.name,
            'region_id': record.region.id,
        }
        return res

    def get_queryset(self):
        return Referee_zone_viewQuerySet(self.model, using=self._db)


class Referee_zone_view(AuditModel, Model_withOldId):
    league = ForeignKeyProtect(Leagues)
    referee = ForeignKeyProtect(Referees)
    region = ForeignKeyProtect(Regions)

    objects = Referee_zone_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        verbose_name = 'Главные судьи в матчах',
        db_table = 'competitions_referee_zones_view'
