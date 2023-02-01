import json

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import ImageInfo
from .modules import get_embedding_diff, get_similar_face
from idealfinder.my_model.main import init_db

from .response import HomeResponse, LookalikeResponse, ProcessResponse, SimilarityResponse
# Create your views here.



class AppHome(APIView):
    def get(self, request):
        return HomeResponse(request).render()

class Process(APIView):
    def get(self, request):
        return ProcessResponse(request).get()

    def post(self, request):
        return ProcessResponse(request).post()

class Similarity(APIView):
    def get(self, request):
        return SimilarityResponse(request).get()

    def post(self, request):
        return SimilarityResponse(request).post()

class Lookalike(APIView):
    def get(self, request):
        return LookalikeResponse(request).get()
        
    def post(self, request):
        return LookalikeResponse(request).post()

class InitDB(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        init_db()
        return redirect("/")