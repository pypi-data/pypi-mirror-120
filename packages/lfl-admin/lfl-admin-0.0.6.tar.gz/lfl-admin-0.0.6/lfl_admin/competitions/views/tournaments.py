from isc_common.common import unknown
from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException , JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.competitions.models.tournaments import Tournaments , TournamentsManager
from lfl_admin.competitions.models.tournaments_view import Tournaments_view , Tournaments_viewManager


@JsonWSResponseWithException()
def Tournaments_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Tournaments_view.objects.
                select_related(*get_relation_field_name( model=Tournaments_view )).
                exclude( code=unknown ).
                get_range_rows1(
                request=request ,
                function=Tournaments_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Tournaments.objects.createFromRequest( request=request , model=Tournaments_view , propsArr=TournamentsManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )\


@JsonResponseWithException()
def Tournaments_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Tournaments.objects.updateFromRequest( request , model=Tournaments_view , propsArr=TournamentsManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Update_4_DivTour( request ) :
    return JsonResponse( DSResponseUpdate( data=Tournaments.objects.updateFromRequest_4_DivTour( request , propsArr=TournamentsManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments_view.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Add_2_favorites( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments_view.objects.get_queryset().add_2_favorites( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_Del_from_favorites( request ) :
    return JsonResponse( DSResponse( request=request , data=Tournaments_view.objects.get_queryset().del_from_favorites( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Tournaments_ImagesUpload( request ) :
    from isc_common.models.upload_image import DSResponse_CommonUploadImage
    from lfl_admin.competitions.models.tournaments_images import Tournaments_images

    DSResponse_CommonUploadImage( request , model=Tournaments , image_model=Tournaments_images )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
