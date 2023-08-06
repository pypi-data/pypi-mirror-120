import logging

from bitfield import BitField
from isc_common.common import undefined , unknown , unknown_name
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds
from isc_common.models.base_ref import BaseRefManager , BaseRefQuerySet , BaseRef

from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class StadiumsQuerySet( BaseRefQuerySet ) :
    pass


class StadiumsManager( BaseRefManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 1
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.constructions.models.stadiums_view import Stadiums_viewManager

        return Stadiums_viewManager.getRecord( record=record )

    def get_queryset( self ) :
        return StadiumsQuerySet( self.model , using=self._db )


class Stadiums( BaseRef , Model_withOldIds ) :
    region = ForeignKeyProtect( Regions )
    props = StadiumsManager.props()

    objects = StadiumsManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.get_or_create(
            code=undefined ,
            region=Regions.unknown()
        )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        res = cls.objects.create(
            props=1 ,
            code=unknown ,
            name=unknown_name ,
            region=Regions.unknown() ,
        )
        return res

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Стадионы'
