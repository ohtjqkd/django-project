from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.api.serializers import UserDisplaySerializer
# Create your views here.


class CurrentUserAPIView(APIView):
    def get(self, request):
        serializer = UserDisplaySerializer
        return Response(serializer.data)