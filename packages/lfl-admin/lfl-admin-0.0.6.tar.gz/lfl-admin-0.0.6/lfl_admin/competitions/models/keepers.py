import logging

from bitfield import BitField
from django.db.models import SmallIntegerField, BigIntegerField, UniqueConstraint, Q
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, Model_withOldIdStr
from isc_common.models.audit_ex import AuditModelEx

from lfl_admin.competitions.models.calendar import Calendar
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.players import Players
from lfl_admin.competitions.models.tournaments import Tournaments

logger = logging.getLogger(__name__)


class KeepersQuerySet(AuditQuerySet):
    pass


class KeepersManager(AuditManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('syncked', 'Синхронизировано'),  # 4
        ), default=0, db_index=True)

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return KeepersQuerySet(self.model, using=self._db)


class Keepers(AuditModelEx, Model_withOldIdStr):
    club = ForeignKeyProtect(Clubs)
    goals = SmallIntegerField()
    match = ForeignKeyProtect(Calendar)
    match_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    player = ForeignKeyProtect(Players)
    player_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    tournament = ForeignKeyProtect(Tournaments)
    tournament_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    props = KeepersManager.props()

    objects = KeepersManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Хранение пропущенных вратарями голов (мячей)'
        constraints = [
            UniqueConstraint(fields=['match', 'player', 'tournament'], condition=Q(match_id_old=None) & Q(player_id_old=None) & Q(tournament_id_old=None), name='Keepers_unique_constraint_0'),
            UniqueConstraint(fields=['match', 'match_id_old', 'player', 'tournament'], condition=Q(player_id_old=None) & Q(tournament_id_old=None), name='Keepers_unique_constraint_1'),
            UniqueConstraint(fields=['match', 'player', 'player_id_old', 'tournament'], condition=Q(match_id_old=None) & Q(tournament_id_old=None), name='Keepers_unique_constraint_2'),
            UniqueConstraint(fields=['match', 'match_id_old', 'player', 'player_id_old', 'tournament'], condition=Q(tournament_id_old=None), name='Keepers_unique_constraint_3'),
            UniqueConstraint(fields=['match', 'player', 'tournament', 'tournament_id_old'], condition=Q(match_id_old=None) & Q(player_id_old=None), name='Keepers_unique_constraint_4'),
            UniqueConstraint(fields=['match', 'match_id_old', 'player', 'tournament', 'tournament_id_old'], condition=Q(player_id_old=None), name='Keepers_unique_constraint_5'),
            UniqueConstraint(fields=['match', 'player', 'player_id_old', 'tournament', 'tournament_id_old'], condition=Q(match_id_old=None), name='Keepers_unique_constraint_6'),
            UniqueConstraint(fields=['match', 'match_id_old', 'player', 'player_id_old', 'tournament', 'tournament_id_old'], name='Keepers_unique_constraint_7'),
        ]
