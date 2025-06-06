from django.db.models.query import Prefetch
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from pass_log.models import Group, Student, Attendance
from pass_log.permissions import IsCuratorOrCaptainOfStudentGroup
from pass_log.serializers import GroupSerializer, GroupListSerializer, StudentSerializer, AttendanceCreateSerializer, \
    AttendanceDisplaySerializer, StudentAttendanceGroupSerializer


# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    """
    Список групп со студентами http://127.0.0.1:8000/group
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class GroupListAPIView(generics.ListAPIView):
    """
    Список групп без студентов http://127.0.0.1:8000/group/list
    """
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    Все запросы связанные со студентами http://127.0.0.1:8000/student
    Включая: Добавление, удаление, обновление и просмотр
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class AttendanceCreateAPIView(generics.CreateAPIView):
    """
    Добавление пропуска http://127.0.0.1:8000/attendance/
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrCaptainOfStudentGroup]


class AttendanceDeleteAPIView(generics.DestroyAPIView):
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated, IsCuratorOrCaptainOfStudentGroup]



class AttendanceDisplayAPIView(generics.ListAPIView):
    """
    Список всех пропусков http://127.0.0.1:8000/attendance/list
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceDisplaySerializer
    permission_classes = [IsAuthenticated]


class AttendanceByStudentView(generics.ListAPIView):
    """
    Список пропусков конкретного студента http://127.0.0.1:8000/attendance/student/<int:student_id>/
    <int:student_id> - идентификатор конкретного студента
    """
    serializer_class = AttendanceDisplaySerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student__id=student_id)


class AttendanceByGroupAndDateRangeView(generics.ListAPIView):
    """
    Список пропусков конкретной группы в конкретный период времени http://127.0.0.1:8000/attendance/group/
    """
    serializer_class = AttendanceDisplaySerializer
    permission_classes = [IsAuthenticated]

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


class AttendanceUpdateView(generics.UpdateAPIView):
    """
    Обновление записи о пропуске http://127.0.0.1:8000/attendance/{id}/
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrCaptainOfStudentGroup]


class AttendanceByGroupAndDateView(generics.ListAPIView):
    """
    Список пропусков конкретной группы в конкретный период времени
    """
    queryset = Student.objects.all()
    serializer_class = StudentAttendanceGroupSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        date = self.request.query_params.get('date')

        if not group_id or not date:
            return Student.objects.none()

        try:
            date = timezone.datetime.strptime(date, '%d.%m.%Y').date()
        except ValueError:
            return Student.objects.none()

        queryset = Student.objects.filter(group__id=group_id)

        attendance_queryset = Attendance.objects.filter(date=date)

        queryset = queryset.prefetch_related(
            Prefetch('attendance', queryset=attendance_queryset)
        )
        return queryset
