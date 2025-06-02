from django.urls import path

from new.views import NewsAPIList

app_name = 'news'

urlpatterns = [
    path('list/', NewsAPIList.as_view(), name='news-list'),
]
