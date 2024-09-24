from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pass_log.apps import PassLogConfig
from pass_log.views import GroupViewSet, GroupListAPIView

app_name = PassLogConfig.name

router = DefaultRouter()
router.register(r'group', GroupViewSet, basename="group")
router.register(r'student', GroupViewSet, basename="student")

urlpatterns = [
    path('', include(router.urls)),
    path('group/list', GroupListAPIView.as_view(), name='group-list'),
]
