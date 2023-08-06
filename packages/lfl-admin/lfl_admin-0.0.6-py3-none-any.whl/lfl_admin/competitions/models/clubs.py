import logging

from bitfield import BitField
from django.db.models import DateField , CheckConstraint , Q , F , BigIntegerField
from isc_common.auth.models.user import User
from isc_common.common import undefined , unknown_name
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldIds
from isc_common.models.base_ref import BaseRefHierarcy , BaseRefHierarcyManager , BaseRefHierarcyQuerySet

from lfl_admin.competitions.models.leagues import Leagues
from lfl_admin.region.models.interregion import Interregion
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class ClubsQuerySet( BaseRefHierarcyQuerySet ) :
    pass


class ClubsManager( BaseRefHierarcyManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'Блокировать клуб') ,  # 1
            ('national' , 'Сборная команда') ,  # 1
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.competitions.models.clubs_view import Clubs_viewManager
        from lfl_admin.competitions.models.clubs_view import Clubs_view
        return Clubs_viewManager.getRecord( record=Clubs_view.objects.get( id=record.id ) )

    def get_queryset( self ) :
        return BaseRefHierarcyQuerySet( self.model , using=self._db )


class Clubs( BaseRefHierarcy , Model_withOldIds ) :
    created_date = DateField( null=True , blank=True )
    editor = ForeignKeyProtect( User , related_name='Clubs_editor' , null=True , blank=True )
    interregion = ForeignKeyProtect( Interregion )
    league = ForeignKeyProtect( Leagues )
    old_superclub_id = BigIntegerField( db_index=True , null=True , blank=True )
    region = ForeignKeyProtect( Regions )

    props = ClubsManager.props()

    objects = ClubsManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=undefined ,
            name=unknown_name ,
            defaults=dict(
                name=unknown_name ,
                interregion=Interregion.unknown() ,
                league=Leagues.unknown() ,
                region=Regions.unknown()
            )
        )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        res = cls.objects.create(
            code=unknown_name ,
            name=unknown_name ,
            interregion=Interregion.unknown() ,
            league=Leagues.unknown() ,
            region=Regions.unknown()
        )

        return res

    def __str__( self ) :
        return f'ID:{self.id} name: {self.name}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Лиги'
        constraints = [
            CheckConstraint( check=~Q( id=F( 'parent_id' ) ) , name=f'c_Clubs' ) ,
        ]
