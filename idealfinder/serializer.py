from rest_framework.serializers import ModelSerializer
from .models import ImageInfo, ClusterInfo, EmbeddingInfo

class ImageInfoSerializers(ModelSerializer):
    class Meta:
        model = ImageInfo
        fileds = "__all__"

class ClusterInfoSerializers(ModelSerializer):
    class Meta:
        model = ClusterInfo
        fields = "__all__"

class EmbeddingInfoSerializers(ModelSerializer):
    class Meta:
        model = EmbeddingInfo
        fields = "__all__"