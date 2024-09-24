from rest_framework import serializers

from pass_log.models import Group, Student


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
