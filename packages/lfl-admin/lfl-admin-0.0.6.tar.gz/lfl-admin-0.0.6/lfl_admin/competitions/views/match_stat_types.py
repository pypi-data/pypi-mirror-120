from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.common.functions import get_relation_field_name

from lfl_admin.competitions.models.match_stat_types import Match_stat_types, Match_stat_typesManager


@JsonResponseWithException()
def Match_stat_types_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Match_stat_types.objects.
                select_related(*get_relation_field_name(model=Match_stat_types)).
                get_range_rows1(
                request=request,
                function=Match_stat_typesManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Add(request):
    return JsonResponse(DSResponseAdd(data=Match_stat_types.objects.createFromRequest(request=request, propsArr=Match_stat_typesManager.props().flags, model=Match_stat_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Update(request):
    return JsonResponse(DSResponseUpdate(data=Match_stat_types.objects.updateFromRequest(request=request, propsArr=Match_stat_typesManager.props().flags, model=Match_stat_types), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Match_stat_types.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Match_stat_types.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Info(request):
    return JsonResponse(DSResponse(request=request, data=Match_stat_types.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Match_stat_types_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Match_stat_types.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
