import logging

from django.db.models import BooleanField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds , AuditModel
from isc_common.models.base_ref import BaseRefManager , BaseRefQuerySet , BaseRef

from lfl_admin.constructions.models.stadiums import Stadiums
from lfl_admin.constructions.models.stadiums import StadiumsManager
from lfl_admin.constructions.models.stadiums_images import Stadiums_images
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class Stadiums_viewQuerySet( BaseRefQuerySet ) :
    pass


class Stadiums_viewManager( BaseRefManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'active' : record.active ,
            'code' : record.code ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'editing' : record.editing ,
            'id' : record.id ,
            'name' : record.name ,
            'props' : record.props ,
            'region__name' : record.region.name ,
            'region_id' : record.region.id ,
        }

        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=[ 'logo' , 'plan' , 'photo' ] ,
            main_model='stadiums' ,
            model='constructions_stadiums' ,
            model_images='constructions_stadiums_images' ,
            imports=[
                'from lfl_admin.constructions.models.stadiums import Stadiums' ,
                'from lfl_admin.constructions.models.stadiums_images import Stadiums_images'
            ] ,
            django_model=Stadiums ,
            django_model_images=Stadiums_images
        )

        return res

    def get_queryset( self ) :
        return Stadiums_viewQuerySet( self.model , using=self._db )


class Stadiums_view( BaseRef , Model_withOldIds ) :
    active = BooleanField()
    region = ForeignKeyProtect( Regions )
    props = StadiumsManager.props()

    objects = Stadiums_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Стадионы'
        db_table = 'constructions_stadiums_view'
        managed = False
