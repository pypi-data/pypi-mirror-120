import logging

from bitfield import BitField
from django.db.models import BigIntegerField, UniqueConstraint, Q
from isc_common.auth.models.user import User
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel, Model_withOldIdStr

from lfl_admin.competitions.models.calendar import Calendar
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.formation import Formation
from lfl_admin.competitions.models.players import Players
from lfl_admin.competitions.models.tournaments import Tournaments

logger = logging.getLogger(__name__)


class Player_historiesQuerySet(AuditQuerySet):
    pass


class Player_historiesManager(AuditManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('game_started', 'game_started'),  # 0
            ('substituted', 'substituted'),  # 1
            ('keeper', 'keeper'),  # 2
            ('hidden', 'Скрывать ФИО'),  # 3
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
        return Player_historiesQuerySet(self.model, using=self._db)


class Player_histories(AuditModel, Model_withOldIdStr):
    club = ForeignKeyProtect(Clubs)
    club_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    editor = ForeignKeyProtect(User, null=True, blank=True)
    formation = ForeignKeyProtect(Formation)
    match = ForeignKeyProtect(Calendar)
    match_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    num = CodeField(null=True, blank=True)
    player = ForeignKeyProtect(Players)
    player_id_old = BigIntegerField(db_index=True, null=True, blank=True)
    props = Player_historiesManager.props()
    tournament = ForeignKeyProtect(Tournaments)

    objects = Player_historiesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Данные об участии игрока в конкретном матче'
        constraints = [
            UniqueConstraint(fields=['club', 'match', 'player'], condition=Q(club_id_old=None) & Q(match_id_old=None) & Q(player_id_old=None), name='Player_histories_unique_constraint_0'),
            UniqueConstraint(fields=['club', 'match', 'match_id_old', 'player'], condition=Q(club_id_old=None) & Q(player_id_old=None), name='Player_histories_unique_constraint_1'),
            UniqueConstraint(fields=['club', 'match', 'player', 'player_id_old'], condition=Q(club_id_old=None) & Q(match_id_old=None), name='Player_histories_unique_constraint_2'),
            UniqueConstraint(fields=['club', 'match', 'match_id_old', 'player', 'player_id_old'], condition=Q(club_id_old=None), name='Player_histories_unique_constraint_3'),
            UniqueConstraint(fields=['club', 'club_id_old', 'match', 'player'], condition=Q(match_id_old=None) & Q(player_id_old=None), name='Player_histories_unique_constraint_4'),
            UniqueConstraint(fields=['club', 'club_id_old', 'match', 'match_id_old', 'player'], condition=Q(player_id_old=None), name='Player_histories_unique_constraint_5'),
            UniqueConstraint(fields=['club', 'club_id_old', 'match', 'player', 'player_id_old'], condition=Q(match_id_old=None), name='Player_histories_unique_constraint_6'),
            UniqueConstraint(fields=['club', 'club_id_old', 'match', 'match_id_old', 'player', 'player_id_old'], name='Player_histories_unique_constraint_7'),
        ]
