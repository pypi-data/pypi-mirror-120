import logging

from django.db.models import TextField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.models.audit import AuditModel , AuditManager , AuditQuerySet

from lfl_admin.competitions.models.clubs import Clubs
from lfl_admin.inventory.models.clothes import Clothes

logger = logging.getLogger( __name__ )


class Clothes_clubsQuerySet( AuditQuerySet ) :

    def update_or_create( self , defaults=None , **kwargs ) :
        from lfl_admin.inventory.models.clothes_type import Clothes_type

        clothes_type = kwargs.get( 'clothes_type' )
        if clothes_type is None :
            raise Exception( 'Не задан параметр clothes_type' )

        club = kwargs.get( 'club' )
        if club is None :
            raise Exception( 'Не задан параметр club' )

        if isinstance( club , int ) :
            club = Clubs.objects.get( id=club )

        code = kwargs.get( 'code' )
        if code is None :
            raise Exception( 'Не задан параметр code' )

        name = kwargs.get( 'name' )
        if name is None :
            raise Exception( 'Не задан параметр name' )

        clothes_context = kwargs.get( 'clothes_context' )

        if not clothes_context :
            return None , None

        clothes_type , _ = Clothes_type.objects.get_or_create( code=clothes_type , defaults=dict( name=clothes_type ) )
        cloth , _ = Clothes.objects.update_or_create(
            clothes_type=clothes_type ,
            code=code ,
            defaults=dict(
                name=name ,
            ) )

        res , created = super().update_or_create( club=club , cloth=cloth , defaults=dict( clothes_context=clothes_context ) )
        logger.debug(f'created: {created}  Clothes_clubs: {res}')
        return res


class Clothes_clubsManager( AuditManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'id' : record.id ,
            'code' : record.code ,
            'name' : record.name ,
            'description' : record.description ,
            'parent' : record.parent.id if record.parent else None ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return Clothes_clubsQuerySet( self.model , using=self._db )

    def get_cloth_context( self , code , club , clothes_type ) :
        from lfl_admin.inventory.models.clothes_type import Clothes_type

        if clothes_type is None :
            raise Exception( 'Не задан параметр clothes_type' )

        if code is None :
            raise Exception( 'Не задан параметр code' )

        if club is None :
            raise Exception( 'Не задан параметр club' )

        if isinstance( club , int ) :
            club = Clubs.objects.get( id=club )

        if isinstance( clothes_type , str ) :
            clothes_type = Clothes_type.objects.get( code=clothes_type )

        cloth = Clothes.objects.get( clothes_type=clothes_type , code=code )

        res = Clothes_clubs.objects.getOptional( club=club , cloth=cloth )
        if res is None :
            return res
        return res.clothes_context


class Clothes_clubs( AuditModel ) :
    club = ForeignKeyProtect( Clubs )
    cloth = ForeignKeyProtect( Clothes )
    clothes_context = TextField( null=True , blank=True )

    objects = Clothes_clubsManager()

    def __str__( self ) :
        return f'ID:{self.id} '

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Кросс таблица'
        unique_together = (('club' , 'cloth') ,)
