import logging
from datetime import timedelta , date

from bitfield import BitField
from django.db.models import DateField , OneToOneField , PROTECT , BooleanField , DateTimeField , SmallIntegerField
from django.utils import timezone
from isc_common.datetime import DateToDateTime , DateToStr
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditManager , AuditQuerySet , AuditModel
from isc_common.models.audit import Model_withOldIds
from isc_common.models.audit_ex import AuditModelEx

from lfl_admin.common.models.posts import Posts
from lfl_admin.competitions.models.referees import Referees
from lfl_admin.competitions.models.referees import RefereesManager
from lfl_admin.competitions.models.referees_images import Referees_images
from lfl_admin.region.models.regions import Regions
from lfl_admin.user_ext.models.contacts import Contacts
from lfl_admin.user_ext.models.persons import Persons

logger = logging.getLogger( __name__ )


class Referees_viewQuerySet( AuditQuerySet ) :
    pass


class Referees_viewManager( AuditManager ) :

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 1
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'active' : record.active ,
            'age' : f'{DateToStr( record.birthday )} ({(timezone.now() - DateToDateTime( record.birthday )) // timedelta( days=365 )})' if isinstance( record.birthday , date ) else None ,
            'debut' : record.debut ,
            'deliting' : record.deliting ,
            'editing' : record.editing ,
            'first_name' : record.first_name ,
            'id' : record.id ,
            'last_name' : record.last_name ,
            'middle_name' : record.middle_name ,
            'name' : record.short_name ,
            'props' : record.props ,
            'qty_leaques' : record.qty_leaques ,
            'referee_post__name' : record.referee_post.name ,
            'referee_post_id' : record.referee_post.id ,
            'region__name' : record.region.name ,
            'region_id' : record.region.id ,
        }
        res = AuditModel.get_urls_datas(
            record=res ,
            # keyimages=[ 'photo11' , 'photo2' , 'photo3' ] ,
            keyimages=[ 'photo11' ] ,
            main_model='referees' ,
            model='competitions_referees' ,
            model_images='competitions_referees_images' ,
            imports=[
                'from lfl_admin.competitions.models.referees import Referees' ,
                'from lfl_admin.competitions.models.referees_images import Referees_images'
            ] ,
            django_model=Referees ,
            django_model_images=Referees_images
        )
        return res

    def get_queryset( self ) :
        return Referees_viewQuerySet( self.model , using=self._db )


class Referees_view( AuditModelEx , Model_withOldIds ) :
    active = BooleanField()
    birthday = DateTimeField( blank=True , null=True )
    contact = ForeignKeyProtect( Contacts )
    debut = DateField( blank=True , null=True )
    first_name = NameField()
    last_name = NameField()
    middle_name = NameField()
    person = OneToOneField( Persons , on_delete=PROTECT )
    props = RefereesManager.props()
    qty_leaques = SmallIntegerField()
    referee_post = ForeignKeyProtect( Posts )
    region = ForeignKeyProtect( Regions , null=True , blank=True )
    short_name = NameField()

    objects = Referees_viewManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.get_or_create( person=Persons.unknown() , defaults=dict( contact=Contacts.unknown() , referee_post=Posts.unknown() ) )
        return res

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Судьи'
        db_table = 'competitions_referees_view'
        managed = False
