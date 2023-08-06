import logging

from django.conf import settings
from django.db.models import SmallIntegerField, CharField, TextField, BooleanField
from isc_common import delAttr, setAttr
from isc_common.auth.models.user import User
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import Model_withOldId, AuditModel
from isc_common.models.base_ref import BaseRefHierarcyManager, BaseRefHierarcyQuerySet, BaseRefHierarcy
from isc_common.number import DelProps, GetListFromStringCortege

from lfl_admin.competitions.models.disqualification_condition import Disqualification_condition
from lfl_admin.competitions.models.disqualification_zones import Disqualification_zones
from lfl_admin.competitions.models.division_stages import Division_stages
from lfl_admin.competitions.models.divisions import DivisionsManager, Divisions
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger(__name__)


class Divisions_viewQuerySet(BaseRefHierarcyQuerySet):
    def prepare_request(self, request):
        from lfl_admin.statistic.models.raiting_of_players_division import Raiting_of_players_division

        data = request.get_data()

        ids = data.get('ids')
        if ids is not None:

            division_id = list(set(map(lambda x: x.get('division'), Raiting_of_players_division.objects.filter(raiting_id__in=ids).values('division'))))
            if len(division_id) == 0:
                division_id = [-1]

            delAttr(request.json.get('data'), 'ids')
            setAttr(request.json.get('data'), 'id', division_id)
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
        data = request.get_data()
        real_id = data.get('real_id')
        if real_id is not None:
            request.set_data(dict(id=real_id))

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


# http://192.168.0.61:8003/logic/Imgs/Download/2607892?code=scheme&path=divisions&main_model=divisions&main_model_id=1182

class Divisions_viewManager(BaseRefHierarcyManager):
    @classmethod
    def getRecord(cls, record):
        from lfl_admin.competitions.models.divisions_images import Divisions_images

        scheme_real_name, scheme_image_src = AuditModel.get_urls_data(
            id=record.id,
            keyimage='scheme',
            main_model='divisions',
            model='competitions_divisions',
            model_images='competitions_divisions_images',
            imports=[
                'from lfl_admin.competitions.models.divisions import Divisions',
                'from lfl_admin.competitions.models.divisions_images import Divisions_images'
            ],
            django_model=Divisions,
            django_model_images=Divisions_images
        )

        scheme_real_name, scheme_image_id = GetListFromStringCortege(scheme_real_name)
        scheme_image_src = f'{settings.IMAGE_CONTENT_PROTOCOL}://{settings.IMAGE_CONTENT_HOST}:{settings.IMAGE_CONTENT_PORT}/{scheme_image_src}'

        res = {
            'active': record.active,
            'code': record.code,
            'deliting': record.deliting,
            'description': record.description,
            'disqualification_condition__name': record.disqualification_condition.name if record.disqualification_condition else None,
            'disqualification_condition_id': record.disqualification_condition.id if record.disqualification_condition else None,
            'division_stages__name': record.stage.name if record.stage else None,
            'division_stages_id': record.stage.name if record.stage else None,
            'editing': record.editing,
            'editor_id': record.editor.id if record.editor else None,
            'editor_short_name': record.editor_short_name,
            'favorites': record.favorites,
            'hidden': record.hidden,
            'icon': "state.png" if record.parent else "division.png",
            'id': record.id,
            'import_model_images': 'from lfl_admin.competitions.models.divisions_images import Divisions_images',
            'is_division': record.is_division,
            'isFolder': record.isFolder,
            'model_images': Divisions_images.__name__,
            'name': record.name,
            'number_of_rounds': record.number_of_rounds,
            'parent_id': record.parent.id if record.parent else None,
            'props': record.props,
            'region__name': record.region.name,
            'region_id': record.region.id,
            'scheme': record.scheme,
            'scheme_image_id': scheme_image_id,
            'scheme_image_src': scheme_image_src,
            'scheme_real_name': scheme_real_name,
            'show_news': record.show_news,
            'stage__name': record.stage.name if record.stage else None,
            'stage_id': record.stage.id if record.stage else None,
            'top_text': record.top_text,
            'zone__name': record.zone.name,
            'zone_id': record.zone.id,
        }
        return DelProps(res)

    def get_queryset(self):
        return Divisions_viewQuerySet(self.model, using=self._db)


class Divisions_view(BaseRefHierarcy, Model_withOldId):
    active = BooleanField()
    completed = BooleanField()
    disqualification_condition = ForeignKeyProtect(Disqualification_condition, null=True, blank=True)
    editor = ForeignKeyProtect(User, related_name='Divisions_view_creator', null=True, blank=True)
    editor_short_name = NameField(null=True, blank=True)
    is_division = BooleanField()
    favorites = BooleanField()
    hidden = BooleanField()
    isFolder = BooleanField()
    number_of_rounds = SmallIntegerField()
    props = DivisionsManager.props()
    region = ForeignKeyProtect(Regions)
    scheme = CharField(null=True, blank=True, max_length=255)
    show_news = BooleanField()
    stage = ForeignKeyProtect(Division_stages, null=True, blank=True)
    top_text = TextField(null=True, blank=True)
    zone = ForeignKeyProtect(Disqualification_zones)

    objects = Divisions_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Супертурниры'
        db_table = 'competitions_divisions_view'
        managed = False
