from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.competitions.models.leagues import Leagues , LeaguesManager
from lfl_admin.competitions.models.leagues_images import Leagues_images
from lfl_admin.competitions.models.leagues_view import Leagues_view , Leagues_viewManager


@JsonResponseWithException()
def Leagues_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Leagues_view.objects.
                select_related( *get_relation_field_name( model=Leagues_view ) ).
                get_range_rows1(
                request=request ,
                function=Leagues_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Leagues.objects.createFromRequest( request=request , model=Leagues_view , propsArr=LeaguesManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Leagues.objects.updateFromRequest( request=request , model=Leagues_view , propsArr=LeaguesManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Leagues.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Leagues.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Leagues.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Leagues.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Leagues_ImagesUpload( request ) :
    from isc_common.models.upload_image import DSResponse_CommonUploadImage

    DSResponse_CommonUploadImage( request , model=Leagues , image_model=Leagues_images )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
