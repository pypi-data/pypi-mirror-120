from isc_common.http.DSResponse import DSResponseUpdate , DSResponseAdd , DSResponse , JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.competitions.models.match_protocol import Match_protocol , Match_protocolManager


@JsonResponseWithException()
def Match_protocol_Fetch( request ) :
    return JsonResponse(
        DSResponse(
            request=request ,
            data=Match_protocol.objects.
                select_related( *get_relation_field_name( model=Match_protocol ) ).
                get_range_rows1(
                request=request ,
                function=Match_protocolManager.getRecord
            ) ,
            status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Add( request ) :
    return JsonResponse( DSResponseAdd( data=Match_protocol.objects.createFromRequest( request=request , propsArr=Match_protocolManager.props() , model=Match_protocol ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Update( request ) :
    return JsonResponse( DSResponseUpdate( data=Match_protocol.objects.updateFromRequest( request=request , propsArr=Match_protocolManager.props() , model=Match_protocol ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Remove( request ) :
    return JsonResponse( DSResponse( request=request , data=Match_protocol.objects.deleteFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Lookup( request ) :
    return JsonResponse( DSResponse( request=request , data=Match_protocol.objects.lookupFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Info( request ) :
    return JsonResponse( DSResponse( request=request , data=Match_protocol.objects.get_queryset().get_info( request=request ) , status=RPCResponseConstant.statusSuccess ).response )


@JsonResponseWithException()
def Match_protocol_Copy( request ) :
    return JsonResponse( DSResponse( request=request , data=Match_protocol.objects.copyFromRequest( request=request ) , status=RPCResponseConstant.statusSuccess ).response )
