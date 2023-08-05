from django.shortcuts import render
from .models import Movie,Actors,Genre,profile2,Favourite
from .serializers import actorsSerailizers,favouriteSerailizers,genreSerailizers,movieSerailizers,ProfileSerializer2
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action,api_view,permission_classes
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

import os
from pytube import YouTube
from django.conf import settings

from django.http import FileResponse
from django.shortcuts import get_object_or_404

class movieViewset(viewsets.ModelViewSet):
    serializer_class=movieSerailizers
    queryset=Movie.objects.all()
    #permission_classes=[IsAuthenticated]
    #authentication_classes=[TokenAuthentication]
    @permission_classes([IsAuthenticated])
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
                serializer = favouriteSerailizers(favourite_obj, many=False, context={'request': request})
                json = {
                'message': 'Movie favourite is updated',
                'result': serializer.data
            }
                return Response(json, status=status.HTTP_201_CREATED)

            except Favourite.DoesNotExist:
                favourite_obj = Favourite.objects.create(favourite=favourite, movie=movie, user=user)
                serializer = favouriteSerailizers(favourite_obj, many=False, context={'request': request})
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
    #permission_classes=[IsAuthenticated]
    #authentication_classes=[TokenAuthentication]
    lookup_field='pk'
class ProfileView(APIView):
   # permission_classes=[IsAuthenticated]
   # authentication_classes=[TokenAuthentication]
    def get(self, request):
        serializer = ProfileSerializer2(request.user.profile2, context={'request': request, 'email': request.user.email, 'password': request.user.password})
        return Response(serializer.data)
    


def download_youtube_video(url):
    yt = YouTube(url)
    video = yt.streams.first()
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', f'{yt.video_id}.mp4')
    video.download(output_path=os.path.dirname(video_path), filename=os.path.basename(video_path))
    return video_path

class MovieUploadAPIView(APIView):
    def post(self, request):
        serializer = movieSerailizers(data=request.data)

        if serializer.is_valid():
            trailer_link = serializer.validated_data.get('trailer_link')
            video_path = download_youtube_video(trailer_link)


            serializer.save(media_file=video_path)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def download_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie_path = movie.file.path
    if os.path.exists(movie_path):
        response = FileResponse(open(movie_path, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(movie_path)}"'
        return response
    trailer_link = movie.trailer_link
    if not trailer_link:
        return Response({"error": "Trailer link not found."}, status=status.HTTP_404_NOT_FOUND)
    video_path = download_youtube_video(trailer_link)
    movie.file = video_path
    movie.save()
    response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'
    return response