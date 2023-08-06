import logging

from isc_common.common import unknown , unknown_name
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

logger = logging.getLogger(__name__)


class Disqualification_conditionQuerySet(BaseRefQuerySet):
    pass

class Disqualification_conditionManager(BaseRefManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Disqualification_conditionQuerySet(self.model, using=self._db)


class Disqualification_condition(BaseRef):
    objects = Disqualification_conditionManager()

    def __str__(self):
        return f'ID:{self.id}'

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=unknown ,
            defaults=dict( name=unknown_name )
        )
        return res

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Условие дисквалификаций'
