from lib2to3.pgen2.tokenize import group

from django.utils import timezone
from rest_framework import viewsets, generics

from pass_log.models import Group, Student, Attendance
from pass_log.serializers import GroupSerializer, GroupListSerializer, StudentSerializer, AttendanceCreateSerializer, \
    AttendanceDisplaySerializer


# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AttendanceCreateAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer


class AttendanceDisplayAPIView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceDisplaySerializer


class AttendanceByStudentView(generics.ListAPIView):
    serializer_class = AttendanceDisplaySerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student__id=student_id)


class AttendanceByGroupAndDateView(generics.ListAPIView):
    serializer_class = AttendanceDisplaySerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = timezone.datetime.strptime(start_date, '%d.%m.%Y').date()
        if end_date:
            end_date = timezone.datetime.strptime(end_date, '%d.%m.%Y').date()

        queryset = Attendance.objects.filter(student__group__id=group_id)

        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset
