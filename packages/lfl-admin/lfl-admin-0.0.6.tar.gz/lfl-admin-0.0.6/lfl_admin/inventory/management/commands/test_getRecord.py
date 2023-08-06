import logging
from operator import itemgetter
from pprint import pprint

from django.core.management import BaseCommand
from isc_common.models.audit import AuditModel

from lfl_admin.inventory.models.clothes import Clothes
from lfl_admin.inventory.models.clothes_images import Clothes_images
from lfl_admin.inventory.models.shirts_view import Shirts_view

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Тест функций применяемых в миграциях"

    images_files = set()
    cnt = 1

    def handle( self , *args , **options ) :
        record = Shirts_view.objects.get( id=4254 )

        res = {
            'active' : record.id ,
            'clothes_type__name' : record.clothes_type.name ,
            'clothes_type_id' : record.clothes_type.id ,
            'code' : record.code ,
            'deliting' : record.deliting ,
            'description' : record.description ,
            'editing' : record.editing ,
            'editor_short_name' : record.editor_short_name ,
            'id' : record.id ,
            'images_data' : record.images_data ,
            'name' : record.name ,
        }

        res = AuditModel.get_urls_datas(
            record=res ,
            keyimages=list( map( lambda x : f'shirts_{x[ 2 ]}' , sorted(record.images_data, key=itemgetter(2)) ) ) if record.images_data is not None else [ ] ,
            main_model='clothes' ,
            model='inventory_clothes' ,
            model_images='inventory_clothes_images' ,
            imports=[
                'from lfl_admin.inventory.models.clothes import Clothes' ,
                'from lfl_admin.inventory.models.clothes_images import Clothes_images'
            ] ,
            django_model=Clothes ,
            django_model_images=Clothes_images ,
            code="shirts",
            add_params=list( map( lambda x : f'position={x[ 2 ]}' , record.images_data ) ) if record.images_data is not None else []
        )

        pprint( res )
