from django.urls import path

from lfl_admin.competitions.views import clubs

urlpatterns = [

    path('Clubs/Fetch/', clubs.Clubs_Fetch),
    path('Clubs/FetchSuper/', clubs.Clubs_FetchSuper),
    path('Clubs/Add', clubs.Clubs_Add),
    path('Clubs/Update', clubs.Clubs_Update),
    path('Clubs/Remove', clubs.Clubs_Remove),
    path('Clubs/Lookup/', clubs.Clubs_Lookup),
    path('Clubs/Info/', clubs.Clubs_Info),
    path('Clubs/Copy', clubs.Clubs_Copy),
    path('Clubs/UploadImage', clubs.Clubs_ImagesUpload),

]
