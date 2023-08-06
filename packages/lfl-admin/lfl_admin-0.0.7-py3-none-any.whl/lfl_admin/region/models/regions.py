import logging

from bitfield import BitField
from django.db.models import CheckConstraint , Q , F
from django.db.models import SmallIntegerField
from isc_common.auth.models.user import User
from isc_common.common import undefined , unknown_name
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefHierarcy , BaseRefQuerySet , BaseRefManager
from isc_common.models.standard_colors import Standard_colors

from lfl_admin.competitions.models.seasons import Seasons
from lfl_admin.region.models.region_zones import Region_zones

logger = logging.getLogger( __name__ )


class RegionsQuerySet( BaseRefQuerySet ) :
    pass

class RegionsManager( BaseRefManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'Актуальность') ,  # 0
            ('select_division' , 'Блокировать регион') ,  # 1
            ('parimatch' , 'parimatch') ,  # 2
            ('submenu' , 'Убрать submenu') ,  # 3
            ('leagues_menu' , 'Отключить выбор дивизиона') ,  # 4
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.region.models.regions_view import Regions_viewManager
        return Regions_viewManager.getRecord( record=record )

    def get_queryset( self ) :
        return RegionsQuerySet( self.model , using=self._db )


class Regions( BaseRefHierarcy , Model_withOldId ) :
    color = ForeignKeyProtect( Standard_colors , null=True , blank=True )
    editor = ForeignKeyProtect( User , null=True , blank=True )
    priority = SmallIntegerField( null=True , blank=True )
    props = RegionsManager.props()
    season = ForeignKeyProtect( Seasons )
    zone = ForeignKeyProtect( Region_zones , null=True , blank=True )

    objects = RegionsManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=undefined ,
            defaults=dict(
                name=unknown_name ,
                season=Seasons.unknown() ,
                zone=Region_zones.unknown()
            ) )
        return res

    def __str__( self ) :
        return f'ID:{self.id}, code: {self.code}, name: {self.name}, description: {self.description}, color: [{self.color}], season: [{self.season}], zone: [{self.zone}], props: [{self.props}]'

    def __repr__( self ) :
        return self.__str__()

    @classmethod
    def get_first_stage_element( cls ) :
        from lfl_admin.region.models.regions_view import Regions_view
        from lfl_admin.region.models.regions_view import Regions_viewManager

        res = cls.objects.create(
            code=unknown_name ,
            name=unknown_name ,
            season=Seasons.unknown() ,
            zone=Region_zones.unknown()
        )
        return res

    class Meta :
        verbose_name = 'Регионы'

        constraints = [
            CheckConstraint( check=~Q( id=F( 'parent_id' ) ) , name=f'c_region' ) ,
        ]
