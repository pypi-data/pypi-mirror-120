from django.urls import path

from lfl_admin.region.views import interregion

urlpatterns = [

    path( 'Interregion/Fetch/' , interregion.Interregion_Fetch ) ,
    path( 'Interregion/Add' , interregion.Interregion_Add ) ,
    path( 'Interregion/Update' , interregion.Interregion_Update ) ,
    path( 'Interregion/Remove' , interregion.Interregion_Remove ) ,
    path( 'Interregion/Lookup/' , interregion.Interregion_Lookup ) ,
    path( 'Interregion/Info/' , interregion.Interregion_Info ) ,
    path( 'Interregion/Copy' , interregion.Interregion_Copy ) ,

]
