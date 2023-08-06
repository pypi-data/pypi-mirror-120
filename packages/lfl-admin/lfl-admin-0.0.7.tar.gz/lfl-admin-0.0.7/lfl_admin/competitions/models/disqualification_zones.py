import logging

from bitfield import BitField
from django.db.models import SmallIntegerField

from isc_common.auth.models.user import User
from isc_common.common import unknown , unknown_name
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet
from isc_common.number import DelProps
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class Disqualification_zonesQuerySet( BaseRefQuerySet ) :
    pass


class Disqualification_zonesManager( BaseRefManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 1
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord(cls, record )  :
        res = {
            'id' : record.id ,
            'code' : record.code ,
            'name' : record.name ,
            'description' : record.description ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
            'region_id' : record.region.id ,
            'region__name' : record.region.name ,
            'props' : record.props ,
            'number_of_yellowsold' : record.number_of_yellowsold ,
        }
        return DelProps( res )

    def get_queryset( self ) :
        return Disqualification_zonesQuerySet( self.model , using=self._db )


class Disqualification_zones( BaseRef , Model_withOldIds ) :
    editor = ForeignKeyProtect( User , null=True , blank=True )
    number_of_yellowsold = SmallIntegerField()
    props = Disqualification_zonesManager.props()
    region = ForeignKeyProtect( Regions )

    objects = Disqualification_zonesManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=unknown ,
            defaults=dict(
                region=Regions.unknown() ,
                number_of_yellowsold = 0,
                name=unknown_name
            ) ,
        )
        return res

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Зоны контроля дисквалификаций'
