import logging

from django.db.models import DateField , BigIntegerField , UniqueConstraint , Q
from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel , AuditManager , AuditQuerySet , Model_withOldIdStr
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.competitions.models.players import Players
from lfl_admin.competitions.models.tournaments import Tournaments

logger = logging.getLogger( __name__ )


class SquadsQuerySet( AuditQuerySet ) :
    pass


class SquadsManager( AuditManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'id' : record.id ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return SquadsQuerySet( self.model , using=self._db )


class Squads( AuditModel , Model_withOldIdStr ) :
    club = ForeignKeyProtect( Clubs )
    deducted = DateField( null=True , blank=True )
    editor = ForeignKeyProtect( User , null=True , blank=True )
    included = DateField( blank=True , null=True )
    player = ForeignKeyProtect( Players )
    tournament = ForeignKeyProtect( Tournaments )
    player_id_old = BigIntegerField( db_index=True , null=True , blank=True )
    club_id_old = BigIntegerField( db_index=True , null=True , blank=True )
    tournament_id_old = BigIntegerField( db_index=True , null=True , blank=True )

    objects = SquadsManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Составы команд'
        constraints = [
            UniqueConstraint( fields=[ 'club' , 'tournament' , 'player' ] , condition=Q( club_id_old=None ) & Q( player_id_old=None ) & Q( tournament_id_old=None ) , name='Squads_unique_constraint_0' ) ,
            UniqueConstraint( fields=[ 'club' , 'tournament' , 'player' , 'tournament_id_old' ] , condition=Q( club_id_old=None ) & Q( player_id_old=None ) , name='Squads_unique_constraint_1' ) ,
            UniqueConstraint( fields=[ 'club' , 'tournament' , 'player' , 'player_id_old' ] , condition=Q( club_id_old=None ) & Q( tournament_id_old=None ) , name='Squads_unique_constraint_2' ) ,
            UniqueConstraint( fields=[ 'club' , 'tournament' , 'player' , 'player_id_old' , 'tournament_id_old' ] , condition=Q( club_id_old=None ) , name='Squads_unique_constraint_3' ) ,
            UniqueConstraint( fields=[ 'club' , 'club_id_old' , 'tournament' , 'player' ] , condition=Q( player_id_old=None ) & Q( tournament_id_old=None ) , name='Squads_unique_constraint_4' ) ,
            UniqueConstraint( fields=[ 'club' , 'club_id_old' , 'tournament' , 'player' , 'tournament_id_old' ] , condition=Q( player_id_old=None ) , name='Squads_unique_constraint_5' ) ,
            UniqueConstraint( fields=[ 'club' , 'club_id_old' , 'tournament' , 'player' , 'player_id_old' ] , condition=Q( tournament_id_old=None ) , name='Squads_unique_constraint_6' ) ,
            UniqueConstraint( fields=[ 'club' , 'club_id_old' , 'tournament' , 'player' , 'player_id_old' , 'tournament_id_old' ] , name='Squads_unique_constraint_7' ) ,
        ]
