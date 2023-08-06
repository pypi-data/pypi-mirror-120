import logging

from django.db.models import Model , Manager , QuerySet , CharField

logger = logging.getLogger( __name__ )


class All_tablesQuerySet( QuerySet ) :
    pass


class All_tablesManager( Manager ) :
    def get_queryset( self ) :
        return All_tablesQuerySet( self.model , using=self._db )


class All_tables( Model ) :
    table_name = CharField( max_length=255 , primary_key=True )

    objects = All_tablesManager()

    def __str__( self ) :
        return self.table_name

    def __repr__( self ) :
        return self.__str__()

    class Meta :
        verbose_name = 'Все пользовательские таблицы'
        db_table = 'all_tables'
        managed = False
