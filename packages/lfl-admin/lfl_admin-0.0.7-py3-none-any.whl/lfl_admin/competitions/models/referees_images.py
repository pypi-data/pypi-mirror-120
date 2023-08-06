import logging

from isc_common.fields.related import ForeignKeyProtect , ForeignKeyCascade
from isc_common.models.audit import AuditManager
from isc_common.models.image_types import Image_types
from isc_common.models.images import Images
from isc_common.models.model_images import Model_imagesQuerySet , Model_images
from lfl_admin.competitions.models.referees import Referees

logger = logging.getLogger(__name__)


class Referees_imagesQuerySet(Model_imagesQuerySet):
    pass


class Referees_imagesManager(AuditManager):

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Referees_imagesQuerySet(self.model, using=self._db)


class Referees_images(Model_images):
    image = ForeignKeyProtect(Images)
    main_model = ForeignKeyCascade(Referees)
    type = ForeignKeyProtect(Image_types)

    objects = Referees_imagesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('image', 'main_model' ,'type', 'deleted_at'),)
