from rest_framework import generics

from new.models import News
from new.serializers import NewsSerializer


class NewsAPIList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
