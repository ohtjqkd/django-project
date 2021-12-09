# from random import random
# from numpy.random.mtrand import random_sample
import json, random
import numpy as np
from idealfinder.models import EmbeddingInfo
from sklearn.cluster import KMeans
from mtcnn.mtcnn import MTCNN
from PIL import Image
from tensorflow.keras.models import load_model

def extract_face(image, required_size=(160, 160), save=False):
    # RGB로 변환, 필요시
    # image = image.convert('RGB')
    # 배열로 변환
    # pixels = np.array(image)
    # 감지기 생성, 기본 가중치 이용
    detector = MTCNN()
    # 이미지에서 얼굴 감지
    results = detector.detect_faces(image)
    # 첫 번째 얼굴에서 경계 상자 추출
    # detect_faces의 결과물 : box, cofidence, keypoints(left_eye, right_eye, nose, mouth_left, mouth_right)
    # 사진 크기가 너무 작아서 detect가 안되는 경우가 있음 -> 우선 그런 영상들을 제외하고 진행
    if len(results)==0:
        return np.asarray([])
    x1, y1, width, height = results[0]['box']
    
    # 버그 수정
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # 얼굴 추출
    face = image[y1:y2, x1:x2]
    # 모델 사이즈로 픽셀 재조정
    # Image.fromarray() : 배열 객체를 입력으로 받아 배열 객체에서 만든 이미지 객체를 반환
    image = Image.fromarray(face)
    image = image.resize(required_size)

    return image

def get_face_embedding(user_img=None, width=None, height=None):
    face_pixels = np.asarray(user_img)
    face_pixels = face_pixels.reshape(height, width, 3).astype(np.uint8)
    face_pixels = np.array(extract_face(face_pixels))
    # 픽셀 값의 척도
    # 채널 간 픽셀값 표준화(전역에 걸쳐)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    # 임베딩을 갖기 위한 예측 생성
    modelFile = '/static/facenet_keras.h5'
    model = load_model(filepath=modelFile)
    user_embedding = model.predict(samples)
    return user_embedding


def get_embedding_diff(user_img, width, height, image_id):
    user_embedding = get_face_embedding(user_img, width, height)
    ideal_embedding = json.loads(EmbeddingInfo.objects.select_related().get(image_id=image_id).embedding)
    return get_score(user_embedding, ideal_embedding)

def get_similar_face(user_img, width, height):
    user_embedding = get_face_embedding(user_img, width, height)
    all_embedding = list(EmbeddingInfo.objects.select_related().all())
    print(len(all_embedding))
    print(all_embedding[0].image)

    all_embedding.sort(key=lambda x: np.linalg.norm(list(map(int, json.loads(x.embedding)))-user_embedding))
    print(all_embedding[:5])
    return list(map(lambda x: f'/static/idealfinder/img/{x.image.gender}/{x.image.get_file_name()}', all_embedding[:5]))

def get_score(a, b):
    return int(((np.dot(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b))))+1)*50)

def kmeans(n_clusters=5, ids=[], embeddings=[]):
    km = KMeans(n_clusters=n_clusters, random_state=42)
    ids = np.array(ids)
    embeddings = np.array(embeddings)
    km.fit(embeddings)
    y_labels = km.labels_
    clusters = []
    for n in range(n_clusters):
        clusters.append([ids[np.where(y_labels==n)], embeddings[np.where(y_labels==n)]])
    return clusters


def get_response(ids=[], embeddings=[], stage=1, choices=[], gender=None):
    stages = [8, 4, 2, 1]
    is_result = (stage == len(stages) or len(embeddings) <= stages[stage-1])
    if is_result:
        clusters = [np.array([ids, embeddings])]
    else:
        clusters = kmeans(n_clusters=stages[stage-1], ids=ids, embeddings=embeddings)
    response = {}
    response['cluster_info'] = {}
    for i, c in enumerate(clusters):
        cluster_ids, cluster_embeddings = c[0], c[1]
        c = list(zip(cluster_ids, cluster_embeddings))
        if stage == len(stages):
            sampled = choices
        else:
            sampled = random.sample(c,1)
        nearest = [n[0] for n in get_near_five(center=sampled, cluster=c, gender=gender, is_result=is_result)]
        response['cluster_info'][i] = {'sample': [s[0] for s in sampled], 'nearest': nearest, 'ids': cluster_ids}
        response['result'] = is_result
    return response

def euclidean_dist(inst1, inst2):
    return np.linalg.norm(inst1-inst2)

def get_near_five(center=[], cluster=[], gender=None, is_result=False):
    embeddings = np.array([np.array(c[1]) for c in center])
    if len(cluster) < 6 and is_result:
        cluster_ = EmbeddingInfo.objects.select_related().filter(image_id_id__gender = gender)
        cluster = [(embedding_info.image_id, json.loads(embedding_info.embedding)) for embedding_info in cluster_]
    average_embed = embeddings.sum(axis=0) / len(center)
    cluster.sort(key=lambda x: euclidean_dist(average_embed, x[1]))
    return cluster[:min(len(cluster), 6)]

