import logging

from django.db.models import DateField , BooleanField , BigIntegerField
from isc_common.auth.models.user import User
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds , AuditModel
from isc_common.models.base_ref import BaseRefHierarcy , BaseRefHierarcyManager , BaseRefHierarcyQuerySet

from lfl_admin.competitions.models.clubs import ClubsManager , Clubs
from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.region.models.interregion import Interregion
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class Clubs_viewQuerySet( BaseRefHierarcyQuerySet ) :
    pass


class Clubs_viewManager( BaseRefHierarcyManager ) :

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.competitions.models.clubs_links import Clubs_links
        from lfl_admin.competitions.models.clubs_images import Clubs_images

        res = {
            'active' : record.active ,
            'code' : record.code ,
            'created_date' : record.created_date ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'editing' : record.editing ,
            'editor_short_name' : record.editor_short_name ,
            'id' : record.id ,
            'interregion__name' : record.interregion.name ,
            'interregion_id' : record.interregion.id ,
            'league__name' : record.league.name ,
            'league_id' : record.league.id ,
            'name' : record.name ,
            'national' : record.national ,
            'parent_id' : record.parent.id if record.parent else None ,
            'region__name' : record.region.name ,
            'region_id' : record.region.id ,
            'site' : Clubs_links.objects.get_link( club=record.id , code='site' )
        }

        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=[ 'logo1' , 'photo' , 'shirt150_1' , 'shirt150_2' , 'shirt150_3' , 'shirt150_4' , 'shirt_keeper1' , 'shirt_keeper2' , 'shirt_winter1' , 'shirt_winter2' ] ,
            main_model='clubs' ,
            model='competitions_clubs' ,
            model_images='competitions_clubs_images' ,
            imports=[
                'from lfl_admin.competitions.models.clubs import Clubs' ,
                'from lfl_admin.competitions.models.clubs_images import Clubs_images'
            ] ,
            django_model=Clubs ,
            django_model_images=Clubs_images
        )

        return res

    def get_queryset( self ) :
        return BaseRefHierarcyQuerySet( self.model , using=self._db )


class Clubs_view( BaseRefHierarcy , Model_withOldIds ) :
    active = BooleanField()
    created_date = DateField( null=True , blank=True )
    editor = ForeignKeyProtect( User , related_name='Clubs_view_editor' , null=True , blank=True )
    editor_short_name = NameField( null=True , blank=True )
    interregion = ForeignKeyProtect( Interregion )
    league = ForeignKeyProtect( Leagues )
    national = BooleanField()
    old_superclub_id = BigIntegerField( db_index=True , null=True , blank=True )
    region = ForeignKeyProtect( Regions )

    props = ClubsManager.props()

    objects = Clubs_viewManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Клубы'
        db_table = 'competitions_clubs_view'
        managed = False
