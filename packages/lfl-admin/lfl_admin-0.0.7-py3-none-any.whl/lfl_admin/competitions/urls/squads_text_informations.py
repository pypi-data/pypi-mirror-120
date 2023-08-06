from django.urls import path

from lfl_admin.competitions.views import squads_text_informations

urlpatterns = [

    path( 'Squads_text_informations/Fetch/' , squads_text_informations.Squads_text_informations_Fetch ) ,
    path( 'Squads_text_informations/Add' , squads_text_informations.Squads_text_informations_Add ) ,
    path( 'Squads_text_informations/Update' , squads_text_informations.Squads_text_informations_Update ) ,
    path( 'Squads_text_informations/Remove' , squads_text_informations.Squads_text_informations_Remove ) ,
    path( 'Squads_text_informations/Lookup/' , squads_text_informations.Squads_text_informations_Lookup ) ,
    path( 'Squads_text_informations/Info/' , squads_text_informations.Squads_text_informations_Info ) ,
    path( 'Squads_text_informations/Copy' , squads_text_informations.Squads_text_informations_Copy ) ,

]
