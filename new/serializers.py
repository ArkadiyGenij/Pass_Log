from rest_framework import serializers

from new.models import NewsImage, News


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'title', 'image', 'create_at', 'update_at']
        read_only_fields = ['create_at', 'update_at']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'preview', 'content', 'create_at', 'update_at', 'is_active', 'images']
        read_only_fields = ['create_at', 'update_at']
