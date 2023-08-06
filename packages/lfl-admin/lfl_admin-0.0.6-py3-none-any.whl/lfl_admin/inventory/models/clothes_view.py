import logging

from django.db.models import BooleanField
from isc_common.auth.models.user import User
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

from lfl_admin.inventory.models.clothes import ClothesManager
from lfl_admin.inventory.models.clothes_type import Clothes_type

logger = logging.getLogger( __name__ )


class Clothes_viewQuerySet( BaseRefQuerySet ) :
    pass


class Clothes_viewManager( BaseRefManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'active' : record.id ,
            'clothes_type__name' : record.clothes_type.name ,
            'clothes_type_id' : record.clothes_type.id ,
            'code' : record.code ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'editing' : record.editing ,
            'editor_short_name' : record.editor_short_name ,
            'id' : record.id ,
            'name' : record.name ,
        }
        return res

    def get_queryset( self ) :
        return Clothes_viewQuerySet( self.model , using=self._db )


class Clothes_view( BaseRef , Model_withOldIds ) :
    active = BooleanField()
    clothes_type = ForeignKeyProtect( Clothes_type )
    editor = ForeignKeyProtect( User , related_name='+' , null=True , blank=True )
    editor_short_name = NameField()
    props = ClothesManager.props()

    objects = Clothes_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Одежда'
        db_table = 'inventory_clothes_view'
        managed = False
