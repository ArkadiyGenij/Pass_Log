from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pass_log.apps import PassLogConfig
from pass_log.views import GroupViewSet, GroupListAPIView, AttendanceCreateAPIView, \
    AttendanceDisplayAPIView, AttendanceByStudentView, AttendanceByGroupAndDateRangeView, StudentViewSet, \
    AttendanceUpdateView, AttendanceByGroupAndDateView, AttendanceDeleteAPIView

app_name = PassLogConfig.name

router = DefaultRouter()
router.register(r'group', GroupViewSet, basename="group")
router.register(r'student', StudentViewSet, basename="student")

urlpatterns = [
    path('', include(router.urls)),
    path('group/list', GroupListAPIView.as_view(), name='group-list'),
    path('attendance/', AttendanceCreateAPIView.as_view(), name='attendance-create'),
    path('attendance/list', AttendanceDisplayAPIView.as_view(), name='attendance-list'),
    path('attendance/student/<int:student_id>/', AttendanceByStudentView.as_view(), name='attendance-by-student'),
    path('attendance/group/range/', AttendanceByGroupAndDateRangeView.as_view(), name='attendance-by-group-and-date-range'),
    path('attendance/group/', AttendanceByGroupAndDateView.as_view(), name='attendance-by-group-and-date'),
    path('attendance/<int:pk>/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendance/delete/<int:pk>', AttendanceDeleteAPIView.as_view(), name='attendance-delete'),
]
