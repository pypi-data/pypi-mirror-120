import logging

from bitfield import BitField
from django.db.models import DateField
from isc_common.common import unknown
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager, AuditQuerySet, Model_withOldIds
from isc_common.models.audit_ex import AuditModelEx

from lfl_admin.common.models.posts import Posts
from lfl_admin.user_ext.models.contacts import Contacts
from lfl_admin.user_ext.models.persons import Persons

logger = logging.getLogger(__name__)


class RefereesQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        username = kwargs.get('person').user.username
        if username != unknown:
            if Referees.objects.getOptional(person = kwargs.get('person')) is not None:
                raise Exception(f'Referees with : {kwargs.get("person")} exists.')
        return super().create(**kwargs)


class RefereesManager(AuditManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('active', 'active'),  # 1
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record):
        from lfl_admin.competitions.models.referees_view import Referees_viewManager
        from lfl_admin.competitions.models.referees_view import Referees_view

        return Referees_viewManager.getRecord(record=Referees_view.objects.get(id=record.id))

    def get_queryset(self):
        return RefereesQuerySet(self.model, using=self._db)


class Referees(AuditModelEx, Model_withOldIds):
    contact = ForeignKeyProtect(Contacts)
    debut = DateField(blank=True, null=True)
    person = ForeignKeyProtect(Persons)
    props = RefereesManager.props()
    referee_post = ForeignKeyProtect(Posts)

    objects = RefereesManager()

    @classmethod
    def unknown(cls):
        res, _ = cls.objects.get_or_create(
            person=Persons.unknown(),
            defaults=dict(
                contact=Contacts.unknown(),
                referee_post=Posts.unknown()
            )
        )
        return res

    @classmethod
    def get_first_stage_element(cls):
        res = cls.objects.create(
            person=Persons.unknown(),
            contact=Contacts.unknown(),
            referee_post=Posts.unknown()
        )

        return res

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Судьи'
