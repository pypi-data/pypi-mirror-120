import logging

from bitfield import BitField
from django.db.models import DateField , SmallIntegerField , OneToOneField , PROTECT
from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel , AuditManager , AuditQuerySet

from lfl_admin.common.models.posts import Posts
from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.user_ext.models.persons import Persons

logger = logging.getLogger( __name__ )


class PlayersQuerySet( AuditQuerySet ) :
    pass


class PlayersManager( AuditManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 0
            ('shadow' , 'Скрыть данные игорока') ,  # 1
            ('blocked' , 'blocked') ,  # 2
            ('disqualification' , 'Дисквалифицирован') ,  # 3 Не задействовано
            ('lockout' , 'Не допущен к играм') ,  # 4
            ('delayed_lockout' , 'Отложенный недопуск') ,  # 5
            ('medical_lockout' , 'medical_lockout') ,  # 6
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.competitions.models.players_view import Players_viewManager
        from lfl_admin.competitions.models.players_view import Players_view

        return Players_viewManager.getRecord( record=Players_view.objects.get( id=record.id ) )

    def get_queryset( self ) :
        return PlayersQuerySet( self.model , using=self._db )


class Players( AuditModel ) :
    amplua = ForeignKeyProtect( Posts )
    club = ForeignKeyProtect( Clubs )
    debut = DateField( null=True , blank=True )
    delayed_lockout_date = DateField( null=True , blank=True )
    editor = ForeignKeyProtect( User , null=True , blank=True )
    height = SmallIntegerField( null=True , blank=True )
    included = DateField( null=True , blank=True )
    medical_admission_date = DateField( null=True , blank=True )
    props = PlayersManager.props()
    number = SmallIntegerField( null=True , blank=True )
    person = OneToOneField( Persons , on_delete=PROTECT )
    weight = SmallIntegerField( null=True , blank=True )

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.get_or_create(
            person=Persons.unknown() ,
            defaults=dict(
                amplua=Posts.unknown() ,
                club_id_now=Clubs.unknown() ,
            )
        )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        res = cls.objects.create(
            person=Persons.unknown() ,
            amplua=Posts.unknown() ,
            club_id_now=Clubs.unknown() ,
        )

        return res

    objects = PlayersManager()

    def __str__( self ) :
        return f'ID:{self.id} full_name = {self.person.user.get_full_name}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Игроки'
