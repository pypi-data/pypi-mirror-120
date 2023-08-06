import logging
from datetime import timedelta, date
from typing import List

from django.db import transaction
from django.db.models import DateField, SmallIntegerField, OneToOneField, PROTECT, BooleanField, DateTimeField
from django.utils import timezone
from isc_common.auth.models.user import User
from isc_common.common.functions import get_dict_only_model_field
from isc_common.datetime import DateToDateTime, DateToStr
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.models.text_informations import Text_informationsManager

from lfl_admin.common.models.posts import Posts
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.players import Players
from lfl_admin.competitions.models.players import PlayersManager
from lfl_admin.competitions.models.players_images import Players_images
from lfl_admin.competitions.models.tournaments import Tournaments
from lfl_admin.region.models.regions import Regions
from lfl_admin.user_ext.models.persons import Persons

logger = logging.getLogger(__name__)


class PlayersQuerySet(AuditQuerySet):
    def prepare_request(self, request):
        from lfl_admin.competitions.models.player_histories import Player_histories

        data = request.get_data()

        division_ids = data.get('division_ids')
        if division_ids is None:
            tounament_ids = data.get('tournaments_ids')
        else:
            tounament_ids = list(set(map(lambda x: x.get('id'), Tournaments.objects.filter(division_id__in=division_ids, props=Tournaments.props.active).values('id'))))

        if tounament_ids is not None:
            player_id = list(set(map(lambda x: x.get('player'), Player_histories.objects.filter(tournament_id__in=tounament_ids).values('player'))))
            if len(player_id) == 0:
                player_id = [-1]

            request.set_data(dict(id=player_id))
        return request

    def get_info(self, request, *args):
        request = DSRequest(request=request)
        request = self.prepare_request(request)

        criteria = self.get_criteria(json=request.json)
        cnt = super().filter(*args, criteria).count()
        cnt_all = super().filter().count()
        return dict(qty_rows=cnt, all_rows=cnt_all)

    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None):
        request = DSRequest(request=request)
        request = self.prepare_request(request)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user
        )
        return res


class Players_viewManager(AuditManager):

    def createFromRequest(self, request, model=None, removed=None, propsArr: List = None):
        from isc_common.auth.managers.user_manager import UserManager

        _request = DSRequest(request=request)
        data = _request.get_data()

        with transaction.atomic():
            user_data = UserManager().createFromRequest(request=request)
            user = User.objects.get(id=user_data.get('id'))
            person = Persons.objects.get_or_create(user=user)
            defaults = get_dict_only_model_field(data=data, model=self.model, exclude=['person'])
            res = super().get_or_create(person=person, editor=_request.user, defaults=defaults)
            res = Players_viewManager.getRecord(Players_view.objects.get(id=res.id))

        return res

    def updateFromRequest(self, request):
        raise Exception('Do not implements')

    def deleteFromRequest(self, request):
        request = DSRequest(request=request)
        tuple_ids = request.get_olds_tuple_ids()
        res = 0
        with transaction.atomic():
            for id, mode in tuple_ids:
                person = super().get(id=id).person
                user = person.user

                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                    person.soft_delete()
                    user.soft_delete()
                    res += 1
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                    person.soft_restore()
                    user.soft_restore()
                else:
                    qty, _ = super().filter(id=id).delete()
                    person.delete()
                    user.delete()
                    res += qty
        return res

    @classmethod
    def getRecord(cls, record):
        _, lockout_reason = Text_informationsManager.get_text(
            model_id=record.id,
            model_code='lockout_reason',
            model='competitions_players',
            model_text='competitions_players_text_informations',
            model_text_fk='player_id'
        )
        _, delayed_lockout_reason = Text_informationsManager.get_text(
            model_id=record.id,
            model_code='delayed_lockout_reason',
            model='competitions_players',
            model_text='competitions_players_text_informations',
            model_text_fk='player_id'
        )

        res = {
            'active': record.active,
            'age': f'{DateToStr(record.birthday)} ({(timezone.now() - DateToDateTime(record.birthday)) // timedelta(days=365)})' if isinstance(record.birthday, date) else None,
            'amplua__name': record.amplua.name,
            'amplua_id': record.amplua.id,
            'club__name': record.club.name,
            'club_id': record.club.id,
            'delayed_lockout_reason': delayed_lockout_reason,
            'deliting': record.deliting,
            'editing': record.editing,
            'first_name': record.first_name,
            'id': record.id,
            'last_name': record.last_name,
            'lockout_reason': lockout_reason,
            'middle_name': record.middle_name,
            'props': record.props,
            'region__name': record.region.name,
            'region_id': record.region.id,
        }
        res = AuditModel.get_urls_datas(
            record=res,
            # keyimages=[ 'photo11' , 'photo2' , 'photo3' ] ,
            keyimages=['photo11'],
            main_model='players',
            model='competitions_players',
            model_images='competitions_players_images',
            imports=[
                'from lfl_admin.competitions.models.players import Players',
                'from lfl_admin.competitions.models.players_images import Players_images'
            ],
            django_model=Players,
            django_model_images=Players_images
        )

        return res

    def get_queryset(self):
        return PlayersQuerySet(self.model, using=self._db)


class Players_view(AuditModel):
    active = BooleanField()
    shadow = BooleanField()
    amplua = ForeignKeyProtect(Posts)
    birthday = DateTimeField(blank=True, null=True)
    club = ForeignKeyProtect(Clubs)
    debut = DateField(null=True, blank=True)
    delayed_lockout_date = DateField(null=True, blank=True)
    editor = ForeignKeyProtect(User, null=True, blank=True)
    first_name = NameField()
    height = SmallIntegerField()
    included = DateField(null=True, blank=True)
    last_name = NameField()
    medical_admission_date = DateField(null=True, blank=True)
    middle_name = NameField()
    number = SmallIntegerField(null=True, blank=True)
    person = OneToOneField(Persons, on_delete=PROTECT)
    region = ForeignKeyProtect(Regions, null=True, blank=True)
    weight = SmallIntegerField()

    props = PlayersManager.props()

    objects = Players_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Игроки'
        db_table = 'competitions_players_view'
        managed = False
