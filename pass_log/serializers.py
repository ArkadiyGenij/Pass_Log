from django.utils import timezone
from rest_framework import serializers

from pass_log.models import Group, Student, Attendance


class AttendanceDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation


class StudentSerializer(serializers.ModelSerializer):
    attendance_count = serializers.SerializerMethodField()
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['name', 'surname', 'attendance_count', 'attendances']

    @staticmethod
    def get_attendance_count(obj):
        return obj.attendance.count()

    @staticmethod
    def get_attendances(obj):
        attendances = obj.attendance.all().order_by('-date')
        return AttendanceDisplaySerializer(attendances, many=True).data


class GroupSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'students', 'students_count']

    @staticmethod
    def get_students_count(obj):
        return obj.students.count()


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', ]


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'pair_number', 'status', ]

    def create(self, validated_data):
        validated_data['date'] = timezone.now().date()
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation
