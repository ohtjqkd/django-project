from django.http.response import JsonResponse
from idealfinder.models import *
from django.shortcuts import redirect, render
# from apps import IdealfinderConfig
import os, random, json
import idealfinder.modules as my_module

class Response:
    def __init__(self, **kargs):
        super.__init__()
        for k, v in kargs:
            setattr(self, k, v)
    def render(self, request):
        return render(request, os.path.join(self.template_path, self.template), context=self.__dict__)
    def json_response(self):
        return JsonResponse({'result': self.param.get('result'), 'render':self.render().content.decode('utf-8')})

class ImageResponse(Response):
    def __init__(self, **kargs):
        super.__init__(kargs)
        self.images_li = []
        self.images_dict = {}
        self.cluster_info_li = []
        self.cluster_info_dict = {}
        self.get_images(gender=self.gender, choices = self.choices)
    
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
        for k, v in params['cluster_info'].items():
            self.cluster_info_dict[i] = {'image_info': ImageInfo.objects.get(id=v.get('sample')[0]), 'nearest': [ImageInfo.objects.get(id=id) for id in v.get('nearest')], 'data': v.get('ids').tolist()}
            i += 1

class HomeResponse(ImageResponse):
    def __init__(self, **kargs):
        super.__init__(**kargs)

class ProcessResponse(ImageResponse):
    def __init__(self, **kargs):
        super.__init__(**kargs)
        self.post_images(gender='male', params=None)
        query_set = ImageInfo.objects.filter(gender=self.gender)
        embedding_info = EmbeddingInfo.objects.select_related().filter(images_id_id__gender = self.gender)
        ids, embeddings = [], []
        for embedding in embedding_info:
            ids.append(embedding.image_id_id)
            embeddings.append(json.loads(embedding_info))
        kmeans_result = my_modules.get_response(ids=ids, embeddings=embeddings)
        return ProcessResponse(request.GET)
    def render(self):
        if self.params.METHOD == 'GET':
            return super
