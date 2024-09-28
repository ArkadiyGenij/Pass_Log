from django.utils import timezone

from rest_framework import serializers

from pass_log.models import Group, Student, Attendance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'surname']


class GroupSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'students', 'students_count']

    def get_students_count(self, obj):
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


class AttendanceDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation
