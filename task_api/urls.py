from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('movie',views.movieViewset,basename='movie')
router.register('movie',views.movieViewset_pk,basename='movie-detail')
urlpatterns=[
     path('profiles/', view=views.ProfileView.as_view(), name='profiles'),
     #path('detail/', view=views.movieViewset_pk, name='movie_detail'),
]
urlpatterns+=router.urls