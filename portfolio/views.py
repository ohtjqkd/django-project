from django.shortcuts import render
from rest_framework.views import APIView
from .apps import PortfolioConfig
# Create your views here.

class AppHome(APIView):
    def get(self, request):
        print('hello')
        print(PortfolioConfig.static_datasource)
        print(type(PortfolioConfig.static_datasource))
        return render(request, 'portfolio/index.html', context=PortfolioConfig.static_datasource)