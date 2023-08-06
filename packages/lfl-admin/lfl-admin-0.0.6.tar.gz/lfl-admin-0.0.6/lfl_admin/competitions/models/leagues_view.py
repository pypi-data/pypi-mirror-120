import logging

from django.db.models import SmallIntegerField , CharField , BooleanField
from isc_common.auth.models.user import User
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId , AuditModel
from isc_common.models.base_ref import BaseRefHierarcyManager , BaseRefHierarcyQuerySet , BaseRef

from lfl_admin.competitions.models.leagues import LeaguesManager
from lfl_admin.competitions.models.seasons import Seasons
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class Leagues_viewQuerySet( BaseRefHierarcyQuerySet ) :
    pass


class Leagues_viewManager( BaseRefHierarcyManager ) :

    @classmethod
    def getRecord( cls , record ) :
        from isc_common.models.model_links import Model_links
        from isc_common.models.text_informations import Text_informationsManager

        _ , bg_link = Model_links.get_link(
            model_id=record.id ,
            model_code='bg_link' ,
            model='competitions_leagues' ,
            model_link='competitions_leagues_links' ,
            model_link_fk='league_id'
        )

        _ , contacts = Text_informationsManager.get_text(
            model_id=record.id ,
            model_code='contacts' ,
            model='competitions_leagues' ,
            model_text='competitions_leagues_text_informations' ,
            model_text_fk='league_id'
        )
        _ , social = Text_informationsManager.get_text(
            model_id=record.id ,
            model_code='social' ,
            model='competitions_leagues' ,
            model_text='competitions_leagues_text_informations' ,
            model_text_fk='league_id'
        )

        res = {
            'active' : record.active ,
            'bg_link' : bg_link ,
            'code' : record.code ,
            'contacts' : contacts ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'editing' : record.editing ,
            'editor_short_name' : record.editor_short_name ,
            'id' : record.id ,
            'name' : record.name ,
            'nonphoto' : record.nonphoto ,
            'props' : record.season.props ,
            'region__name' : record.region.name ,
            'region_id' : record.region.id ,
            'season__name' : record.season.name ,
            'season_id' : record.season.id ,
            'show_in_menu' : record.show_in_menu ,
            'show_referee_photo_in_protocols' : record.show_referee_photo_in_protocols ,
            'show_shirt_in_protocols' : record.show_shirt_in_protocols ,
            'show_stadium_photo_in_protocols' : record.show_stadium_photo_in_protocols ,
            'slideshow_title' : record.slideshow_title ,
            'social' : social ,
            'submenu' : record.submenu ,
        }

        from lfl_admin.competitions.models.leagues_images import Leagues_images
        from lfl_admin.competitions.models.leagues import Leagues

        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=[ 'header' , 'logo' ] ,
            main_model='leagues' ,
            model='competitions_leagues' ,
            model_images='competitions_leagues_images' ,
            imports=[
                'from lfl_admin.competitions.models.leagues import Leagues' ,
                'from lfl_admin.competitions.models.leagues_images import Leagues_images'
            ] ,
            django_model=Leagues ,
            django_model_images=Leagues_images
        )
        return res

    def get_queryset( self ) :
        return BaseRefHierarcyQuerySet( self.model , using=self._db )


class Leagues_view( BaseRef , Model_withOldId ) :
    active = BooleanField()
    add_slideshow_tabs = CharField( max_length=255 , null=True , blank=True )
    code = CodeField( verbose_name='Краткое название' )
    editor = ForeignKeyProtect( User , null=True , blank=True )
    editor_short_name = NameField( null=True , blank=True )
    nonphoto = BooleanField()
    position = SmallIntegerField( default=1 )
    props = LeaguesManager.props()
    referees_max = SmallIntegerField( default=1 )
    region = ForeignKeyProtect( Regions )
    season = ForeignKeyProtect( Seasons )
    show_in_menu = BooleanField()
    show_referee_photo_in_protocols = BooleanField()
    show_shirt_in_protocols = BooleanField()
    show_stadium_photo_in_protocols = BooleanField()
    slideshow_title = CharField( max_length=255 , null=True , blank=True )
    submenu = BooleanField()

    objects = Leagues_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Лиги'
        db_table = 'competitions_leagues_view'
        managed = False
