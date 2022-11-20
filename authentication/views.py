from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer


class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []


class TestView(APIView):

    def get(self, request):
        data = {"test" : "hello"}
        return  Response(data)