from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.models.upload_image import DSResponse_CommonUploadImage
from lfl_admin.user_ext.models.administrators import Administrators , AdministratorsManager


@JsonResponseWithException()
def Administrators_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Administrators.objects.
                select_related(*get_relation_field_name( model=Administrators )).
                get_range_rows1(
                request=request ,
                function=AdministratorsManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Administrators.objects.createFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Administrators.objects.updateFromRequest( request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Administrators.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Administrators.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Administrators.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Administrators.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Administrators_ImagesUpload( request ) :
    from isc_common.models.users_images import Users_images
    DSResponse_CommonUploadImage( request , model=Administrators , image_model=Users_images , field_main_model='user' )
    return JsonResponse( dict( status=RPCResponseConstant.statusSuccess ) )
