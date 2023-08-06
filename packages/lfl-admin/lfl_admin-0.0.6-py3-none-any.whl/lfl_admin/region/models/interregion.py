import logging

from isc_common.common import undefined , unknown_name
from isc_common.models.audit import Model_withOldId
from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

logger = logging.getLogger( __name__ )


class InterregionQuerySet( BaseRefQuerySet ) :
    pass


class InterregionManager( BaseRefManager ) :

    @classmethod
    def getRecord( cls , record ) :
        res = {
            'id' : record.id ,
            'code' : record.code ,
            'name' : record.name ,
            'description' : record.description ,
            'editing' : record.editing ,
            'deliting' : record.deliting ,
        }
        return res

    def get_queryset( self ) :
        return InterregionQuerySet( self.model , using=self._db )


class Interregion( BaseRef , Model_withOldId ) :
    objects = InterregionManager()

    def __str__( self ) :
        return f'ID:{self.id}'

    def __repr__( self ) :
        return self.__str__()

    @classmethod
    def unknown( cls ) :
        res , _ = cls.objects.update_or_create(
            code=undefined ,
            defaults=dict(
                name=unknown_name ,
            ) )
        return res

    class Meta :
        verbose_name = 'Меж регион'
