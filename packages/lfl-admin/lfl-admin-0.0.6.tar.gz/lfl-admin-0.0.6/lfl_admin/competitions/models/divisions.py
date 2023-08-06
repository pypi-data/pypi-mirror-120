import logging

from bitfield import BitField
from django.db.models import SmallIntegerField , CharField , TextField , CheckConstraint , F , Q
from isc_common import setAttr
from isc_common.auth.models.user import User
from isc_common.common import unknown , unknown_name
from isc_common.fields.code_field import CodeStrictField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRefHierarcyManager , BaseRefHierarcyQuerySet , BaseRefHierarcy

from lfl_admin.competitions.models.disqualification_condition import Disqualification_condition
from lfl_admin.competitions.models.disqualification_zones import Disqualification_zones
from lfl_admin.competitions.models.division_stages import Division_stages
from lfl_admin.region.models.regions import Regions

logger = logging.getLogger( __name__ )


class DivisionsQuerySet( BaseRefHierarcyQuerySet ) :
    def create( self , **kwargs ) :
        parent = kwargs.get( 'parent' )
        if parent is None and kwargs.get( 'parent_id' ) is not None :
            parent = self.get( id=kwargs.get( 'parent_id' ) )
        if kwargs.get( 'stage_id' ) is not None :
            stage = Division_stages.objects.get( id=kwargs.get( 'stage_id' ) )
            setAttr( kwargs , 'code' , stage.code )
            setAttr( kwargs , 'name' , stage.name )
        if kwargs.get( 'region_id' ) is None and parent is not None :
            setAttr( kwargs , 'region' , parent.region )
        if kwargs.get( 'zone_id' ) is None and parent is not None :
            setAttr( kwargs , 'zone' , parent.zone )
        if parent is not None and parent.disqualification_condition is not None :
            setAttr( kwargs , 'disqualification_condition' , parent.disqualification_condition )
        return super().create( **kwargs )

    def update( self , **kwargs ) :
        if kwargs.get( 'stage_id' ) is not None :
            stage = Division_stages.objects.get( id=kwargs.get( 'stage_id' ) )
            setAttr( kwargs , 'code' , stage.code )
            setAttr( kwargs , 'name' , stage.name )
        return super().update( **kwargs )


class DivisionsManager( BaseRefHierarcyManager ) :
    def updateFromRequest_4_DivTour( self , request , removed=None , function=None , propsArr=None ) :
        from lfl_admin.competitions.models.tournaments_division_view import Tournaments_division_view
        from lfl_admin.competitions.models.tournaments_division_view import Tournaments_division_viewManager

        res = self._updateFromRequest( request=request , removed=removed , function=function , propsArr=propsArr )
        record = Tournaments_division_view.objects.get( id=res.id )
        res = Tournaments_division_viewManager.getRecord( record=record )
        return res

    @classmethod
    def props( cls ) :
        return BitField( flags=(
            ('active' , 'active') ,  # 0
            ('completed' , 'completed') ,  # 1
            ('show_news' , 'show_news') ,  # 2
            ('favorites' , 'Избранные') ,  # 3
            ('hidden' , 'Скрывать ФИО') ,  # 4
            ('notConfirmed' , 'Новый не подтвержденный') ,  # 5
        ) , default=1 , db_index=True )

    @classmethod
    def getRecord( cls , record ) :
        from lfl_admin.competitions.models.divisions_view import Divisions_viewManager
        return Divisions_viewManager.getRecord( record=record )

    def get_queryset( self ) :
        return DivisionsQuerySet( self.model , using=self._db )


class Divisions( BaseRefHierarcy , Model_withOldId ) :
    code = CodeStrictField()
    disqualification_condition = ForeignKeyProtect( Disqualification_condition , null=True , blank=True )
    editor = ForeignKeyProtect( User , related_name='Divisions_creator' , null=True , blank=True )
    number_of_rounds = SmallIntegerField( null=True , blank=True )
    props = DivisionsManager.props()
    region = ForeignKeyProtect( Regions )
    scheme = CharField( null=True , blank=True , max_length=255 )
    stage = ForeignKeyProtect( Division_stages , null=True , blank=True )
    top_text = TextField( null=True , blank=True )
    zone = ForeignKeyProtect( Disqualification_zones )

    objects = DivisionsManager()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=unknown ,
            disqualification_condition=Disqualification_condition.unknown() ,
            number_of_rounds=0 ,
            props=1 ,
            region=Regions.unknown() ,
            zone=Disqualification_zones.unknown() ,
            defaults=dict( name=unknown_name )
        )
        return res

    @classmethod
    def get_first_stage_element( cls ) :
        res = cls.objects.create(
            code=unknown ,
            name=unknown_name ,
            disqualification_condition=Disqualification_condition.unknown() ,
            number_of_rounds=0 ,
            props=cls.props.active | cls.props.notConfirmed ,
            region=Regions.unknown() ,
            zone=Disqualification_zones.unknown() ,
        )
        return res

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Супертурниры'
        constraints = [
            CheckConstraint( check=~Q( id=F( 'parent_id' ) ) , name=f'c_Divisions' ) ,
        ]
