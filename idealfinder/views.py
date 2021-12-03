from django.shortcuts import render
from rest_framework.views import APIView
from idealfinder.apps import HomeConfig
from .response import HomeResponse

# Create your views here.
class AppHome(APIView):
    def get(self, request):
        choices = request.GET.get('choices', '')
        gender = request.GET.get('gender', '')
        return HomeResponse.render()