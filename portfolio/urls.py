from django.urls import path, include
import portfolio.views as views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('user', views.UserViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.AppHome.as_view()),
]