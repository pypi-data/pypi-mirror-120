import logging

from django.db.models import TextField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

from lfl_admin.competitions.models.clubs import Clubs

logger = logging.getLogger( __name__ )


class Inventory_clubs_clothes_viewQuerySet( BaseRefQuerySet ) :
    pass


class Inventory_clubs_clothes_viewManager( BaseRefManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'id' : record.id ,
            'code' : record.code ,
            'name' : record.name ,
            'description' : record.description ,
            'clothes_context' : record.clothes_context ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return Inventory_clubs_clothes_viewQuerySet( self.model , using=self._db )


class Inventory_clubs_clothes_view( BaseRef ) :
    clothes_context = TextField(null=True, blank=True)
    club = ForeignKeyProtect( Clubs )
    objects = Inventory_clubs_clothes_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Форма клуба'
        managed = False
        db_table = 'inventory_clubs_clothes_view'
