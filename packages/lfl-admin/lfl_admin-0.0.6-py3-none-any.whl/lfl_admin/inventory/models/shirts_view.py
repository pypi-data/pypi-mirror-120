import logging
from operator import itemgetter

from django.contrib.postgres.fields import ArrayField
from django.db.models import BooleanField , BigIntegerField
from isc_common.auth.models.user import User
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds , AuditModel
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

from lfl_admin.inventory.models.clothes import ClothesManager , Clothes
from lfl_admin.inventory.models.clothes_images import Clothes_images
from lfl_admin.inventory.models.clothes_type import Clothes_type

logger = logging.getLogger( __name__ )


class Shirts_viewQuerySet( BaseRefQuerySet ) :
    pass


class Shirts_viewManager( BaseRefManager ) :

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
            'images_data' : record.images_data ,
            'name' : record.name ,
        }
        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=list( map( lambda x : f'shirts_{x[ 2 ]}' , sorted( record.images_data , key=itemgetter( 2 ) ) ) ) if record.images_data is not None else [ ] ,
            main_model='clothes' ,
            model='inventory_clothes' ,
            model_images='inventory_clothes_images' ,
            imports=[
                'from lfl_admin.inventory.models.clothes import Clothes' ,
                'from lfl_admin.inventory.models.clothes_images import Clothes_images'
            ] ,
            django_model=Clothes ,
            django_model_images=Clothes_images ,
            code="shirts" ,
            add_params=list( map( lambda x : f'position={x[ 2 ]}' , record.images_data ) ) if record.images_data is not None else [ ]
        )
        return res

    def get_queryset( self ) :
        return Shirts_viewQuerySet( self.model , using=self._db )


class Shirts_view( BaseRef , Model_withOldIds ) :
    active = BooleanField()
    clothes_type = ForeignKeyProtect( Clothes_type )
    editor = ForeignKeyProtect( User , related_name='+' , null=True , blank=True )
    editor_short_name = NameField()
    images_data = ArrayField( ArrayField( BigIntegerField() ) )
    props = ClothesManager.props()

    objects = Shirts_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Майки'
        db_table = 'inventory_shirts_view'
        managed = False
