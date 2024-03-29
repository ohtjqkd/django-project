from django.http.response import JsonResponse
from idealfinder.models import *
from idealfinder.apps import *
from django.shortcuts import redirect, render
# from apps import IdealfinderConfig
import os, random, json, datetime, time
from idealfinder.modules import get_response, get_embedding_diff, get_similar_face

class Response:
    def __init__(self, request, **kwargs):
        self.request = request
        self.template_path = "idealfinder"
        self.app = "idealfinder"
        self.css_list = ['common.css']
        self.js_list = ['util.js']
        for k, v in kwargs.items():
            setattr(self, k, v)
    def render(self):
        print(self.template_path)
        return render(self.request, os.path.join(self.template_path, self.template), context=self.__dict__)
    def json_response(self):
        return JsonResponse({'result': self.params.get('result'), 'render':self.render().content.decode('utf-8')})

class ImageResponse(Response):
    def __init__(self, request, **kargs):
        super().__init__(request, **kargs)
        self.images_li = []
        self.images_dict = {}
        self.cluster_info_li = []
        self.cluster_info_dict = {}
        # self.get_images(gender=self.gender, choices = self.choices)
    
    def get_images(self, gender='', choices=''):
        stage_n_cluster = [6, 5, 5]
        if gender == '':
            curr_cluster = ClusterInfo.objects.select_related().filter(cluster__startswith=choices)
        else:
            curr_cluster = ClusterInfo.objects.select_related().filter(image_id__gender=gender, cluster__startswith=choices)
        if len(choices) == len(stage_n_cluster)-1 or len(curr_cluster) == 1:
            self.chain_page = self.next_point
        for i in range(stage_n_cluster[len(choices)]):
            try:
                next_choice = self.choices + str(i)
                i_cluster = curr_cluster.filter(cluster__startswith=next_choice)
                curr_cand = i_cluster[random.randint(0, len(i_cluster)-1)]
                self.cluster_info_li.append(curr_cand)
            except Exception as e:
                print(e)
    def post_images(self, gender='male', params=None):
        i = 0
        print(params)
        for k, v in params.get('cluster_info', {}).items():
            self.cluster_info_dict[i] = {'image_info': ImageInfo.objects.get(id=v.get('sample')[0]), 'nearest': [ImageInfo.objects.get(id=id) for id in v.get('nearest')], 'data': v.get('ids').tolist()}
            i += 1

class HomeResponse(ImageResponse):
    def __init__(self, request, **kargs):
        super().__init__(request, **kargs)
        self.template = 'index.html'
        self.css_list.append('index.css')
        self.js_list.append('index.js')
        self.gender = self.request.GET.get('gender', '')

class ProcessResponse(ImageResponse):
    def __init__(self, request, **kargs):
        super().__init__(request, **kargs)
        self.template = 'process.html'
        self.css_list.append('process.css')
        self.js_list.append('process.js')
        self.gender = self.request.GET.get('gender', '')

    def get(self):
        self.template = 'process.html'
        ids, embeddings = [], []
        for embedding in EmbeddingInfo.objects.select_related().filter(image_id__gender = self.gender):
            print(embedding)
            ids.append(embedding.image_id)
            embeddings.append(json.loads(embedding.embedding))
        self.stage = 1
        self.params = get_response(ids=ids, embeddings=embeddings)
        self.post_images(self.gender, self.params)
        return self.render()

    def post(self):
        request_time = datetime.datetime.now()
        body = self.request.data
        self.stage = int(body.get('stage', 1))+1
        curr_selected_sample, selected_ids, selected_embeddings = [], [], []
        for k, v in body.get('selected').items():
            try:
                selected_ids.extend(list(map(int, v[1:-1].split(", "))))
                curr_selected_sample.append((int(k), json.loads(EmbeddingInfo.objects.get(image_id = int(k)).embedding)))
            except Exception as e:
                print(e)
        for id in selected_ids:
            selected_embeddings.append(json.loads(EmbeddingInfo.objects.get(image_id=id).embedding))
        self.params = get_response(ids=selected_ids, embeddings=selected_embeddings, stage=self.stage, choices=curr_selected_sample, gender=self.gender)
        if self.params['result']:
            self.template = 'result.html'
        else:
            self.template = 'process_response.html'
        self.post_images(self.gender, self.params)
        time.sleep(max(0, 2-(datetime.datetime.now()-request_time).seconds))
        return self.json_response()

class SimilarityResponse(Response):
    def __init__(self, request, **kwargs):
        super().__init__(request, **kwargs)
        self.template = 'similarity.html'
        self.css_list.append('similarity.css')
        self.js_list.append('similarity.js')

    def get(self):
        self.image_info = ImageInfo.objects.get(id=self.request.GET.get('id'))
        return self.render()
    
    def post(self):
        self.image_id = self.request._request.GET.get('id')
        body = self.request.data
        user_img = list(map(int, body.get('user_img').split(',')))
        width, height = body.get('width'), body.get('height')
        self.selector = 'span.score-int'
        self.attr = 'innerText'
        msg = 'success'
        try:
            self.value = get_embedding_diff(user_img, width, height, self.image_id)
        except Exception as e:
            self.msg = e
            self.value = '??'
        return self.json_response()

class LookalikeResponse(Response):
    def __init__(self, request, **kwargs):
        super().__init__(request, **kwargs)
        self.template = 'lookalike.html'
        self.css_list.append('lookalike.css')
        self.js_list.append('lookalike.js')

    def get(self):
        self.range = range(5)
        return self.render()
    
    def post(self):
        body = self.request.data
        user_img = list(map(int, body.get('user_img').split(',')))
        width, height = body.get('width'), body.get('height')
        self.value = get_similar_face(user_img, width, height)
        self.selector, self.attr = "imag#imageTest", "src"
        return self.json_response()