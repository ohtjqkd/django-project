import json

from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import ImageInfo
from .modules import get_embedding_diff, get_similar_face
from idealfinder.my_model.main import init_db

from .response import HomeResponse, ProcessResponse
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
        sim_response = {}
        sim_response['image_info'] = ImageInfo.objects.get(id=request.GET.get('id'))
        print(sim_response)
        return render(request, 'idealfinder/similarity_myimg.html', context=sim_response)
    def post(self, request):
        image_id = request._request.GET.get("id")
        json_body = json.loads(request.body)
        user_img = list(map(int, json_body.get('user_img').split(",")))
        width = json_body.get('width')
        height = json_body.get('height')
        status_code = 200
        try:
            score = get_embedding_diff(user_img, width, height, image_id)
        except Exception as e:
            print(e)
            score = '??'
            status_code = 400

        return JsonResponse(data={"selector":"span.score-int", "attr": "innerText", "values": [score]})

class Neighbor(APIView):
    def get(self, request):
        nei_response = {'range':range(5)}
        return render(request, 'idealfinder/similarface.html', context=nei_response)
    def post(self, request):
        json_body = json.loads(request.body)
        user_img = list(map(int, json_body.get('user_img').split(",")))
        width = json_body.get('width')
        height = json_body.get('height')
        image_info = get_similar_face(user_img, width, height)
        print(image_info)
        return JsonResponse(data={"selector":"img#imageTest", "attr": "src", "values": image_info})

class InitDB(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        init_db()
        return redirect("/")