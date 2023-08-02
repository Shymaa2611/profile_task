from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password




class Genre(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name
class Actors(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title=models.CharField(max_length=100)
    rated=models.DecimalField(max_digits=10,decimal_places=3)
    duration2=models.IntegerField(default=0,verbose_name='duration',)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    poster=models.ImageField(upload_to='movies/poster/',blank=True,null=True)
    trailer_link=models.CharField(max_length=200,blank=True,null=True)
    genre=models.ManyToManyField(Genre)
    actors=models.ManyToManyField(Actors)
    class Meta:
        ordering=['-created_at']
    def __str__(self):
        return self.title
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    favourite = models.BooleanField(default=False)

class profile2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    favorites = models.ManyToManyField(Favourite, blank=True,verbose_name='Favorite movies')
    def __str__(self):
        return f'{self.user.username} Profile'
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = profile2.objects.create(
            user=kwargs['instance'],
            email=kwargs['instance'].email,
            password=make_password(kwargs['instance'].password),
        )
        favorite_movies = Favourite.objects.filter(user=kwargs['instance'], favourite=True)
        if favorite_movies is not None:
            print("there is not favorite movies")
        else:
         user_profile.favourites.set(favorite_movies)

post_save.connect(create_profile,sender=User)




    

