import logging

from django.db.models import BooleanField , TextField , SmallIntegerField
from isc_common.auth.models.user import User
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId , AuditModel
from isc_common.models.base_ref import BaseRefHierarcy , BaseRefQuerySet , BaseRefManager
from isc_common.models.standard_colors import Standard_colors

from lfl_admin.competitions.models.seasons import Seasons
from lfl_admin.region.models.region_images import Region_images
from lfl_admin.region.models.region_zones import Region_zones
from lfl_admin.region.models.regions import Regions
from lfl_admin.region.models.regions import RegionsManager

logger = logging.getLogger( __name__ )


class Regions_viewQuerySet( BaseRefQuerySet ) :
    pass


class Regions_viewManager( BaseRefManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'active' : record.active ,
            'code' : None ,
            'color__color' : record.color.color if record.color else None ,
            'color__name' : record.color.name if record.color else None ,
            'color_id' : record.color.id if record.color else None ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'contacts' : record.contacts ,
            'editing' : record.editing ,
            'editor_short_name' : record.editor_short_name ,
            'editor_id' : record.editor.id if record.editor else None ,
            'id' : record.id ,
            'name' : record.name ,
            'parent' : record.parent.id if record.parent else None ,
            'priority' : record.priority ,
            'season__name' : record.season.name ,
            'season_id' : record.season.id ,
            'zone__name' : record.zone.name if record.zone else None ,
            'zone_id' : record.zone.id if record.zone else None ,
        }

        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=[ 'logo' , 'header' ] ,
            main_model='regions' ,
            model='region_regions' ,
            model_images='region_region_images' ,
            imports=[
                'from lfl_admin.region.models.regions import Regions' ,
                'from lfl_admin.region.models.region_images import Region_images'
            ] ,
            django_model=Regions ,
            django_model_images=Region_images
        )
        return res

    def get_queryset( self ) :
        return Regions_viewQuerySet( self.model , using=self._db )


class Regions_view( BaseRefHierarcy , Model_withOldId ) :
    active = BooleanField()
    color = ForeignKeyProtect( Standard_colors , null=True , blank=True )
    contacts = TextField( null=True , blank=True )
    editor = ForeignKeyProtect( User , null=True , blank=True )
    editor_short_name = NameField( null=True , blank=True )
    leagues_menu = BooleanField( verbose_name='leagues_menu' )
    priority = SmallIntegerField( null=True , blank=True )
    props = RegionsManager.props()
    season = ForeignKeyProtect( Seasons )
    select_division = BooleanField( verbose_name='Блокировать регион' )
    submenu = BooleanField( verbose_name='Убрать submenu' )
    zone = ForeignKeyProtect( Region_zones , null=True , blank=True )

    objects = Regions_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}, color: [{self.color}], season: [{self.season}], zone: [{self.zone}], props: [{self.props}]'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Регионы'
        db_table = 'region_region_view'
        managed = False
