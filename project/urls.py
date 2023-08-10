
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
SpectacularAPIView,
SpectacularRedocView,
SpectacularSwaggerView, # new
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('task_api.urls')),
    path('users/',include('accounts.urls')),
    path('api/token/', obtain_auth_token, name='api-token'),
  #path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
  #path("api/schema/redoc/", SpectacularRedocView.as_view(
  # url_name="schema"), name="redoc",),
  #path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(
   #  url_name="schema"), name="swagger-ui"), 
    #path("api-auth/", include("rest_framework.urls"))
]
# Media setting #
if settings.DEBUG is True:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


