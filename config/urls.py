"""djangoportfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.http.response import HttpResponseRedirect
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
urlpatterns = [
    path('', lambda x: HttpResponseRedirect('portfolio')),
    path('admin/', admin.site.urls),
    path('api/', include('user.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/obtain_token/', obtain_jwt_token, name='obtain-jwt'),
    path('api/rest-auth/refresh_token/', refresh_jwt_token, name='refresh-jwt'),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('idealfinder/', include('idealfinder.urls')),
]