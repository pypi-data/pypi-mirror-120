from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.region.models.interregion import Interregion , InterregionManager


@JsonResponseWithException()
def Interregion_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Interregion.objects.
                filter().
                get_range_rows1(
                request=request ,
                function=InterregionManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Interregion.objects.createFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Interregion.objects.updateFromRequest( request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Interregion.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Interregion.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Interregion.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Interregion_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Interregion.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )
