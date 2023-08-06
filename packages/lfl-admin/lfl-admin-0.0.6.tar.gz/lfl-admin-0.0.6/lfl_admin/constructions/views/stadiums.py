from isc_common.common import undefined
from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.constructions.models.stadiums import Stadiums , StadiumsManager
from lfl_admin.constructions.models.stadiums_view import Stadiums_view , Stadiums_viewManager


@JsonResponseWithException()
def Stadiums_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Stadiums_view.objects.
                select_related( *get_relation_field_name( model=Stadiums_view ) ).
                exclude( code=undefined ).
                get_range_rows1(
                request=request ,
                function=StadiumsManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Stadiums.objects.createFromRequest( request=request , propsArr=StadiumsManager.props() , model=Stadiums_view ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Stadiums.objects.updateFromRequest( request=request , propsArr=StadiumsManager.props() , model=Stadiums_view ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Stadiums.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Stadiums.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Stadiums.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Stadiums.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Stadiums_ImagesUpload( request ) :
    from isc_common.models.upload_image import DSResponse_CommonUploadImage
    from lfl_admin.constructions.models.stadiums_images import Stadiums_images

    DSResponse_CommonUploadImage( request , model=Stadiums , image_model=Stadiums_images )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
