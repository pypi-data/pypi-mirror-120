from isc_common.common.functions import get_relation_field_name
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from lfl_admin.user_ext.models.persons import Persons
from lfl_admin.user_ext.models.persons_view import Persons_viewManager, Persons_view


@JsonResponseWithException()
def Persons_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Persons_view.objects.
                select_related(*get_relation_field_name( model=Persons_view )).
                get_range_rows1(
                request=request,
                function=Persons_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Add(request):
    return JsonResponse(DSResponseAdd(data=Persons.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Update(request):
    return JsonResponse(DSResponseUpdate(data=Persons.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Persons.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Persons.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Info(request):
    return JsonResponse(DSResponse(request=request, data=Persons_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Persons_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Persons.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
