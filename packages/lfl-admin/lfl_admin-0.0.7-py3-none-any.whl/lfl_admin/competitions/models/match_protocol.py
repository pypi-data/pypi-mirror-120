import logging

from django.db.models import Model , BigIntegerField , BooleanField , SmallIntegerField
from isc_common.fields.name_field import NameField
from isc_common.models.audit import AuditManager , AuditQuerySet

logger = logging.getLogger( __name__ )


class Match_protocolQuerySet( AuditQuerySet ) :
    pass


class Match_protocolManager( AuditManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'amplua__name' : record.amplua__name ,
            'assists' : record.assists ,
            'autogoals' : record.autogoals ,
            'club__name' : record.club__name ,
            'club_id' : record.club_id ,
            'dyellow_cards' : record.dyellow_cards ,
            'fouls_penalty' : record.fouls_penalty ,
            'game_started' : record.game_started ,
            'goals' : record.goals ,
            'keeper' : record.keeper ,
            'keeper_goarls' : record.keeper_goarls ,
            'match_id' : record.match_id ,
            'nongoals' : record.nongoals ,
            'penalties_nonsaved' : record.penalties_nonsaved ,
            'penalties_saved' : record.penalties_saved ,
            'pgoals' : record.pgoals ,
            'player_name' : record.player_name ,
            'red_cards' : record.red_cards ,
            'squad' : record.squad ,
            'yellow_cards' : record.yellow_cards ,
        }
        return res

    def get_queryset( self ) :
        return Match_protocolQuerySet( self.model , using=self._db )


class Match_protocol( Model ) :
    pk = None
    amplua_name = NameField()
    assists = SmallIntegerField( blank=True , null=True )
    autogoals = SmallIntegerField( blank=True , null=True )
    club_name = NameField()
    club_id = BigIntegerField()
    dyellow_cards = SmallIntegerField( blank=True , null=True )
    fouls_penalty = SmallIntegerField( blank=True , null=True )
    game_started = BooleanField( blank=True , null=True )
    goals = SmallIntegerField( blank=True , null=True )
    keeper = BooleanField( blank=True , null=True )
    keeper_goarls = SmallIntegerField( blank=True , null=True )
    match_id = BigIntegerField()
    nongoals = SmallIntegerField( blank=True , null=True )
    penalties_nonsaved = SmallIntegerField( blank=True , null=True )
    penalties_saved = SmallIntegerField( blank=True , null=True )
    pgoals = SmallIntegerField( blank=True , null=True )
    player_name = NameField()
    red_cards = SmallIntegerField( blank=True , null=True )
    squad = BooleanField( blank=True , null=True )
    yellow_cards = SmallIntegerField( blank=True , null=True )

    objects = Match_protocolManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Протокол матча'
        managed = False
        db_table = 'competitions_match_protocol_view'
