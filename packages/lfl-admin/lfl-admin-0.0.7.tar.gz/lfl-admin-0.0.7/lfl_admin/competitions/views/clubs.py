from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.competitions.models.clubs import Clubs , ClubsManager
from lfl_admin.competitions.models.clubs_view import Clubs_viewManager , Clubs_view


@JsonResponseWithException()
def Clubs_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Clubs_view.objects.
                select_related( *get_relation_field_name( model=Clubs_view ) ).
                get_range_rows1(
                request=request ,
                function=Clubs_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_FetchSuper( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Clubs_view.objects.
                select_related( *get_relation_field_name( model=Clubs ) ).
                get_range_rows1(
                request=request ,
                function=Clubs_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Clubs.objects.createFromRequest( request=request , propsArr=ClubsManager.props() , model=Clubs_view ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Clubs.objects.updateFromRequest( request=request, propsArr=ClubsManager.props() , model=Clubs_view ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Clubs.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Clubs.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Clubs_view.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Clubs_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Clubs.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )

@JsonResponseWithException()
def Clubs_ImagesUpload( request ) :
    from isc_common.models.upload_image import DSResponse_CommonUploadImage
    from lfl_admin.competitions.models.clubs_images import Clubs_images

    DSResponse_CommonUploadImage( request , model=Clubs , image_model=Clubs_images )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
