from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from .apps import PortfolioConfig

# Create your views here.

class AppHome(APIView):
    def get(self, request):
        return render(request, 'portfolio/index.html', context=PortfolioConfig.static_datasource)