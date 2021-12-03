from django.urls import path
import portfolio.views as views

urlpatterns = [
    path('', views.AppHome.as_view()),
]