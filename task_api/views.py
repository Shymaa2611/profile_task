from django.shortcuts import render
from .models import Movie,Actors,Genre,profile2,Favourite
from .serializers import actorsSerailizers,favouriteSerailizers,genreSerailizers,movieSerailizers,ProfileSerializer2
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics

class movieViewset(viewsets.ModelViewSet):
    serializer_class=movieSerailizers
    queryset=Movie.objects.all()
    @action(methods=['POST'], detail=True)
    def movie_favourite(self, request, pk=None):
        if 'favourite' in request.data:
            movie = Movie.objects.get(pk=pk)
            favourite = request.data['favourite']
            username = request.data['username']
            user = User.objects.get(username=username)
            try:
                favourite_obj = Favourite.objects.get(user=user, movie=movie.pk)
                favourite_obj.favourite = favourite
                favourite_obj.save()
                serializer = favouriteSerailizers(favourite_obj, many=False)
                json = {
                'message': 'Movie favourite is updated',
                'result': serializer.data
            }
                return Response(json, status=status.HTTP_201_CREATED)

            except Favourite.DoesNotExist:
                favourite_obj = Favourite.objects.create(favourite=favourite, movie=movie, user=user)
                serializer = favouriteSerailizers(favourite_obj, many=False)
                json = {
                'message': 'Successfully added',
                'result': serializer.data
            }
                return Response(json, status=status.HTTP_200_OK)

        else:
            json = {
                'message': 'Invalid request'
          }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

class movieViewset_pk(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=movieSerailizers
    lookup_field='pk'
class ProfileView(APIView):
    def get(self, request):
        serializer = ProfileSerializer2(request.user.profile2, context={'request': request, 'email': request.user.email, 'password': request.user.password})
        return Response(serializer.data)