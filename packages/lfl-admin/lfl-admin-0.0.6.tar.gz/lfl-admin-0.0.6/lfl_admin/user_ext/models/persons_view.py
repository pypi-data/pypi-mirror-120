import logging
from typing import List

from django.conf import settings
from django.db import transaction
from django.db.models import OneToOneField, PROTECT, BooleanField, DateField
from isc_common.auth.models.user import User
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager, AuditQuerySet, Model_withOldIds
from isc_common.models.audit_ex import AuditModelEx
from isc_common.number import DelProps

from lfl_admin.region.models.regions import Regions
from lfl_admin.user_ext.models.persons import PersonsManager

logger = logging.getLogger(__name__)


class Persons_viewQuerySet(AuditQuerySet):
    pass


class Persons_viewManager(AuditManager):

    def createFromRequest(self, request, model=None, removed=None, propsArr: List = None):
        from isc_common.auth.managers.user_manager import UserManager

        _request = DSRequest(request=request)

        with transaction.atomic():
            user_data = UserManager().createFromRequest(request=request)
            user = User.objects.get(id=user_data.get('id'))
            res = super().create(user=user, editor=_request.user)
            res = Persons_viewManager.getRecord(Persons_view.objects.get(id=res.id))

        return res

    def updateFromRequest(self, request):
        raise Exception('Do not implements')

    def deleteFromRequest(self, request):
        request = DSRequest(request=request)
        tuple_ids = request.get_olds_tuple_ids()
        res = 0
        with transaction.atomic():
            for id, mode in tuple_ids:
                user = super().get(id=id).user
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                    user.soft_delete()
                    res += 1
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                    user.soft_restore()
                else:
                    qty, _ = super().filter(id=id).delete()
                    user.delete()
                    res += qty
        return res

    @classmethod
    def getRecord(cls, record):
        res = {
            'active': record.active,
            'archive': record.archive,
            'birthday': record.birthday,
            'deliting': record.deliting,
            'description': record.description,
            'editing': record.editing,
            'first_name': record.first_name,
            'id': record.id,
            'last_name': record.last_name,
            'middle_name': record.middle_name,
            'photo_real_name': record.photo_real_name,
            'photo_src': f'{settings.IMAGE_CONTENT_PROTOCOL}://{settings.IMAGE_CONTENT_HOST}:{settings.IMAGE_CONTENT_PORT}/{record.photo_image_src}&ws_host={settings.WS_HOST}&ws_port={settings.WS_PORT}&ws_channel={settings.WS_CHANNEL}',
            'props': record.props,
            'region__name': record.region.name,
            'region_id': record.region.id,
        }
        return DelProps(res)

    def get_queryset(self):
        return Persons_viewQuerySet(self.model, using=self._db)


class Persons_view(AuditModelEx, Model_withOldIds):
    active = BooleanField()
    archive = BooleanField()
    birthday = DateField(blank=True, null=True)
    description = DescriptionField()
    editor_short_name = NameField()
    first_name = NameField()
    last_name = NameField()
    middle_name = NameField()
    photo_image_src = NameField()
    photo_real_name = NameField()
    props = PersonsManager.props()
    region = ForeignKeyProtect(Regions, null=True, blank=True)
    user = OneToOneField(User, on_delete=PROTECT)

    objects = Persons_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Персоны'
        db_table = 'user_ext_persons_view'
        managed = False
