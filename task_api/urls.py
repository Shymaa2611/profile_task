from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('movie',views.movieViewset,basename='movie')
router.register('movie',views.movieViewset_pk,basename='movie-detail')
urlpatterns=[
     path('profiles/', view=views.ProfileView.as_view(), name='profiles'),
     path('movies/<int:pk>/download/',view=views.MovieDownloadView.as_view(), name='download_movie'),
     path('movies/upload/', view=views.MovieUploadAPIView.as_view(), name='movie-upload'),
]
urlpatterns+=router.urls