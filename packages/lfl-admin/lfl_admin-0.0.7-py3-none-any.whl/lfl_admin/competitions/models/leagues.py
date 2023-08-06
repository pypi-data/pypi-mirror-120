import logging

from bitfield import BitField
from django.db.models import SmallIntegerField , CharField
from isc_common.auth.models.user import User
from isc_common.common import undefined , unknown_name
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefHierarcyManager , BaseRefHierarcyQuerySet , BaseRef

from lfl_admin.competitions.models.seasons import Seasons
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class LeaguesQuerySet( BaseRefHierarcyQuerySet ) :
    pass


class LeaguesManager( BaseRefHierarcyManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 0
            ('parimatch' , 'parimatch') ,  # 1
            ('submenu' , 'Убрать submenu') ,  # 2
            ('nonphoto' , 'Разрешить заявки без фото') ,  # 3
            ('show_in_menu' , 'Показывать в правом меню') ,  # 4
            ('show_referee_photo_in_protocols' , 'Показывать фото судей в протоколах') ,  # 5
            ('show_stadium_photo_in_protocols' , 'Показывать фото стадиона в протоколах') ,  # 6
            ('show_shirt_in_protocols' , 'Показывать майки в протоколах') ,  # 7
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.competitions.models.leagues_view import Leagues_viewManager
        return Leagues_viewManager.getRecord( record=record )

    def get_queryset( self ) :
        return BaseRefHierarcyQuerySet( self.model , using=self._db )


class Leagues( BaseRef , Model_withOldId ) :
    add_slideshow_tabs = CharField( max_length=255 , null=True , blank=True )
    code = CodeField()
    editor = ForeignKeyProtect( User , null=True , blank=True )
    position = SmallIntegerField( default=1 )
    props = LeaguesManager.props()
    referees_max = SmallIntegerField( default=1 )
    region = ForeignKeyProtect( Regions )
    season = ForeignKeyProtect( Seasons )
    slideshow_title = CharField( max_length=255 , null=True , blank=True )

    objects = LeaguesManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=undefined ,
            defaults=dict(
                name=unknown_name ,
                season=Seasons.unknown() ,
                region=Regions.unknown()
            ) )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        from lfl_admin.competitions.models.leagues_view import Leagues_view
        from lfl_admin.competitions.models.leagues_view import Leagues_viewManager

        res = cls.objects.create(
            code=unknown_name ,
            name=unknown_name ,
            season=Seasons.unknown() ,
            region=Regions.unknown()
        )

        return res

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Лиги'
