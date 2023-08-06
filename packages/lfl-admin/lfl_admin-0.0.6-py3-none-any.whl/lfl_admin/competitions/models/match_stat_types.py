import logging

from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefQuerySet, BaseRefManager, BaseRef

logger = logging.getLogger(__name__)


class Match_stat_typesQuerySet(BaseRefQuerySet):
    pass


class Match_stat_typesManager(BaseRefManager):

    @classmethod
    def getRecord(cls, record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
            'code': record.code,
            'name': record.name,
        }
        return res

    def get_queryset(self):
        return Match_stat_typesQuerySet(self.model, using=self._db)


class Match_stat_types(BaseRef, Model_withOldId):
    objects = Match_stat_typesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Типы статистики матча'
