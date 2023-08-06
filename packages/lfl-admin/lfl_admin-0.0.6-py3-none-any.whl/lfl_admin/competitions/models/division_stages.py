import logging

from isc_common.models.base_ref import BaseRef , BaseRefManager , BaseRefQuerySet

logger = logging.getLogger( __name__ )


class Division_stagesQuerySet( BaseRefQuerySet ) :
    pass


class Division_stagesManager( BaseRefManager ) :

    @classmethod
    def getRecord(cls, record )  :
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
        return Division_stagesQuerySet( self.model , using=self._db )


class Division_stages( BaseRef ) :
    objects = Division_stagesManager()

    def __str__( self ) :
        return f'ID:{self.id}, code: {self.code}, name: {self.name}'

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Эапы супертурнира'
