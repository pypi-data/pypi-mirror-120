import logging
import uuid

from bitfield import BitField
from isc_common.auth.models.user import User
from isc_common.common import undefined , unknown_name
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

from lfl_admin.inventory.models.clothes_type import Clothes_type

logger = logging.getLogger( __name__ )


class ClothesQuerySet( BaseRefQuerySet ) :
    pass


class ClothesManager( BaseRefManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'Актуальность') ,  # 1
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.inventory.models.clothes_view import Clothes_viewManager
        from lfl_admin.inventory.models.clothes_view import Clothes_view

        return Clothes_viewManager.getRecord( record=Clothes_view.objects.get( id=record.id ) )

    def get_queryset( self ) :
        return ClothesQuerySet( self.model , using=self._db )


class Clothes( BaseRef , Model_withOldIds ) :
    editor = ForeignKeyProtect( User , related_name='+' , null=True , blank=True )
    clothes_type = ForeignKeyProtect( Clothes_type )
    props = ClothesManager.props()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.get_or_create(
            code=undefined ,
            defaults=dict(
                name=unknown_name ,
                clothes_type=Clothes_type.unknown() ,
            ) )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        res = cls.objects.create(
            code=str( uuid.uuid4() ) ,
            name=unknown_name ,
            clothes_type=Clothes_type.unknown() ,
        )
        return res

    objects = ClothesManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Одежда'
