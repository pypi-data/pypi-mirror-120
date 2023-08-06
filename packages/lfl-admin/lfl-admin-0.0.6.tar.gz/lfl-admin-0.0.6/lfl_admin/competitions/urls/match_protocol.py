from django.urls import path

from lfl_admin.competitions.views import match_protocol

urlpatterns = [

    path( 'Match_protocol/Fetch/' , match_protocol.Match_protocol_Fetch ) ,
    path( 'Match_protocol/Add' , match_protocol.Match_protocol_Add ) ,
    path( 'Match_protocol/Update' , match_protocol.Match_protocol_Update ) ,
    path( 'Match_protocol/Remove' , match_protocol.Match_protocol_Remove ) ,
    path( 'Match_protocol/Lookup/' , match_protocol.Match_protocol_Lookup ) ,
    path( 'Match_protocol/Info/' , match_protocol.Match_protocol_Info ) ,
    path( 'Match_protocol/Copy' , match_protocol.Match_protocol_Copy ) ,

]
