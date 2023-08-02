from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('movie',views.movieViewset,basename='movie')
urlpatterns=[
     path('profiles/', view=views.ProfileView.as_view(), name='profiles'),
     #path('favourite/', view=views.FavouriteListAPIView.as_view(), name='favourite'),
]
urlpatterns+=router.urls