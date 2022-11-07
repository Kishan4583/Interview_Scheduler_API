from .serializers import InterviewDetailsSerializer
from .serializers import UserDetailsSerializer
from rest_framework import generics
from rest_framework import status
from .models import User_Info, Interview_Info
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from .emailnotifications import Notify
import pytz
import datetime
from django.http import HttpResponse

# assuming that currently admin users are only accessing the website
def getCurrentTime():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)


@api_view(['GET'])
def getInterviewsbyusers(request, pk):
    currentTime = getCurrentTime()
    queryset = Interview_Info.objects.filter(
        participants=pk, endTime__gte=currentTime).order_by('startTime')
    serializer = InterviewDetailsSerializer(queryset, many=True)
    return Response(serializer.data)


class manageusersList(generics.ListCreateAPIView):
    queryset = User_Info.objects.all()
    serializer_class = UserDetailsSerializer


class manageusersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User_Info.objects.all()
    serializer_class = UserDetailsSerializer


@api_view(['GET', 'POST'])
def manageInterviewsList(request):
    if request.method == 'GET':
        currentTime = getCurrentTime()
        queryset = Interview_Info.objects.filter(
            endTime__gte=currentTime).order_by('startTime')
        serializer = InterviewDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = InterviewDetailsSerializer(data=request.data)
        if serializer.is_valid() and serializer.checkCreateoverlapping():
            serializer.save()
            newData = serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.error_messages)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def manageInterviewsDetail(request, pk):
    try:
        Interview = Interview_Info.objects.get(pk=pk)
    except Interview_Info.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InterviewDetailsSerializer(Interview)
        return Response(serializer.data)

    elif request.method == 'PUT':
        oldserializer = InterviewDetailsSerializer(Interview)
        oldData = oldserializer.data
        serializer = InterviewDetailsSerializer(Interview, data=request.data)
        if serializer.is_valid() and serializer.checkUpdateoverlappings(oldData['id']):
            serializer.save()
            newData = serializer.data
            oldData = oldserializer.data
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        serializer = InterviewDetailsSerializer(Interview)
        oldData = serializer.data
        Interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

