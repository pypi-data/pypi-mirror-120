from django.urls import path

from lfl_admin.inventory.views import inventory_clubs_clothes_view

urlpatterns = [

    path( 'Inventory_clubs_clothes_view/Fetch/' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Fetch ) ,
    path( 'Inventory_clubs_clothes_view/Add' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Add ) ,
    path( 'Inventory_clubs_clothes_view/Update' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Update ) ,
    path( 'Inventory_clubs_clothes_view/Remove' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Remove ) ,
    path( 'Inventory_clubs_clothes_view/Lookup/' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Lookup ) ,
    path( 'Inventory_clubs_clothes_view/Info/' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Info ) ,
    path( 'Inventory_clubs_clothes_view/Copy' , inventory_clubs_clothes_view.Inventory_clubs_clothes_view_Copy ) ,

]
