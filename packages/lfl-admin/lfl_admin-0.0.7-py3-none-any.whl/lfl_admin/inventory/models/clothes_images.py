import logging

from bitfield import BitField
from django.db.models import IntegerField

from isc_common.fields.related import ForeignKeyProtect , ForeignKeyCascade
from isc_common.models.audit import Model_withOldId
from isc_common.models.image_types import Image_types
from isc_common.models.images import Images
from isc_common.models.model_images import Model_imagesManager , Model_imagesQuerySet , Model_images
from lfl_admin.inventory.models.clothes import Clothes

logger = logging.getLogger(__name__)


class Clothes_imagesQuerySet(Model_imagesQuerySet):
    pass


class Clothes_imagesManager(Model_imagesManager):
    @classmethod
    def props(cls):
        return BitField(flags=(
            ('active', 'Актуальность'),  # 1
        ), default=1, db_index=True)

    @classmethod
    def getRecord(cls, record ) :
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Clothes_imagesQuerySet(self.model, using=self._db)


class Clothes_images(Model_images, Model_withOldId):
    image = ForeignKeyProtect(Images)
    main_model = ForeignKeyCascade(Clothes)
    position = IntegerField()
    props = Clothes_imagesManager.props()
    type = ForeignKeyProtect(Image_types)

    objects = Clothes_imagesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Кросс таблица'
        unique_together = (('main_model', 'image', 'type', 'deleted_at'),)
