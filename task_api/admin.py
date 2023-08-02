from django.contrib import admin
from .models import Actors,Favourite,Genre,profile2,Movie

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(profile2)
admin.site.register(Actors)
admin.site.register(Favourite)
