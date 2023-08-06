from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException , JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.competitions.models.divisions import Divisions , DivisionsManager
from lfl_admin.competitions.models.divisions_view import Divisions_view , Divisions_viewManager


@JsonWSResponseWithException()
def Divisions_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Divisions_view.objects.
                select_related( *get_relation_field_name( model=Divisions_view ) ).
                get_range_rows1(
                request=request ,
                function=Divisions_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Divisions.objects.createFromRequest( request=request , propsArr=DivisionsManager.props() , model=Divisions_view ) , status=RPCResponseConstant.statusSuccess ).response )

@JsonResponseWithException()
def Divisions_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Divisions.objects.updateFromRequest( request=request , propsArr=DivisionsManager.props() , model=Divisions_view ) , status=RPCResponseConstant.statusSuccess ).response )

@JsonResponseWithException()
def Divisions_Update_4_DivTour( request ) :
    return JsonResponse( DSResponseUpdate( data=Divisions.objects.updateFromRequest_4_DivTour( request , propsArr=DivisionsManager.props() ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Divisions.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Divisions.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Divisions_view.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Divisions.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Divisions_ImagesUpload( request ) :
    from isc_common.models.upload_image import DSResponse_CommonUploadImage
    from lfl_admin.competitions.models.divisions_images import Divisions_images

    DSResponse_CommonUploadImage( request , model=Divisions , image_model=Divisions_images )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
