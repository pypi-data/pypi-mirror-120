from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from lfl_admin.inventory.models.inventory_clubs_clothes_view import Inventory_clubs_clothes_view , Inventory_clubs_clothes_viewManager


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Inventory_clubs_clothes_view.objects.
                filter().
                order_by( 'clothes_context' ).
                get_range_rows1(
                request=request ,
                function=Inventory_clubs_clothes_viewManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Inventory_clubs_clothes_view.objects.createFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Inventory_clubs_clothes_view.objects.updateFromRequest( request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Inventory_clubs_clothes_view.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Inventory_clubs_clothes_view.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Inventory_clubs_clothes_view.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Inventory_clubs_clothes_view_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Inventory_clubs_clothes_view.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )
