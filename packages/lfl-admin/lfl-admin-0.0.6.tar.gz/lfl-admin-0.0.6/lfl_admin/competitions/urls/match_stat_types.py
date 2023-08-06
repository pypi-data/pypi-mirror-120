from django.urls import path

from lfl_admin.competitions.views import match_stat_types

urlpatterns = [

    path('Match_stat_types/Fetch/', match_stat_types.Match_stat_types_Fetch),
    path('Match_stat_types/Add', match_stat_types.Match_stat_types_Add),
    path('Match_stat_types/Update', match_stat_types.Match_stat_types_Update),
    path('Match_stat_types/Remove', match_stat_types.Match_stat_types_Remove),
    path('Match_stat_types/Lookup/', match_stat_types.Match_stat_types_Lookup),
    path('Match_stat_types/Info/', match_stat_types.Match_stat_types_Info),
    path('Match_stat_types/Copy', match_stat_types.Match_stat_types_Copy),

]
