from rest_framework import serializers
from .models import Favourite,Genre,Actors,profile2,Movie
from django.contrib.auth.models import User

class movieSerailizers(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)
    actors = serializers.StringRelatedField(many=True)
    Duration= serializers.IntegerField(source='duration2')
    class Meta:
        model = Movie
        fields = ('title', 'rated', 'Duration', 'description', 'poster', 'trailer_link', 'genre', 'actors')
class genreSerailizers(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'

class actorsSerailizers(serializers.ModelSerializer):
    class Meta:
        model=Actors
        fields='__all__'



class ProfileSerializer2(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    email = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    Favorite_movies = serializers.SerializerMethodField()

    class Meta:
        model = profile2
        fields = ['user', 'email', 'password', 'Favorite_movies']

    def get_email(self, obj):
        return self.context['email']

    def get_password(self, obj):
        return self.context['password']

    def get_Favorite_movies(self, obj):
        favourites = Favourite.objects.filter(user=obj.user, favourite=True)
        serializer = favouriteSerailizers(favourites, many=True)
        return serializer.data
class favouriteSerailizers(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = Favourite
        fields = ['movie']