import logging

from bitfield import BitField
from django.db.models import IntegerField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.image_types import Image_types
from isc_common.models.images import Images
from isc_common.models.model_images import Model_imagesQuerySet , Model_images , Model_imagesManager

from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.user_ext.models.persons import Persons

logger = logging.getLogger( __name__ )


class Person_club_photosQuerySet( Model_imagesQuerySet ) :
    pass


class Person_club_photosManager( Model_imagesManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('main' , 'main') ,  # 1
        ) , default=0 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'id' : record.id ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return Person_club_photosQuerySet( self.model , using=self._db )


class Person_club_photos( Model_images , Model_withOldId ) :
    club = ForeignKeyProtect( Clubs )
    image = ForeignKeyProtect( Images )
    main_model = ForeignKeyProtect( Persons )
    num = IntegerField( null=True , blank=True )
    props = Person_club_photosManager.props()
    type = ForeignKeyProtect( Image_types )

    objects = Person_club_photosManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Кросс таблица'
