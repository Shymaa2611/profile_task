from rest_framework import serializers
from .models import Favourite,Genre,Actors,profile2,Movie
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class movieSerailizers(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True,read_only=True)
    actors = serializers.StringRelatedField(many=True,read_only=True)
    Duration= serializers.IntegerField(source='duration2')
    file = serializers.FileField(read_only=True)
    class Meta:
        model = Movie
        fields = ('title', 'rated', 'Duration', 'description', 'poster', 'trailer_link', 'genre', 'actors','file','media_file')
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
        serializer = favouriteSerailizers(favourites, many=True, context=self.context)
        return serializer.data
class favouriteSerailizers(serializers.ModelSerializer):
    movie = serializers.HyperlinkedRelatedField(
        view_name='movie-detail',
        read_only=True,
        lookup_field='pk'
    )

    class Meta:
        model = Favourite
        fields = ['movie']