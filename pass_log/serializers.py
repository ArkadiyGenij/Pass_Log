from rest_framework import serializers

from pass_log.models import Group, Student, Attendance


class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'surname']


class AttendanceDisplaySerializer(serializers.ModelSerializer):
    student = StudentInfoSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'date', 'pair_number', 'status', 'student']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation


class AttendanceDisplayGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'pair_number', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation


class StudentSerializer(serializers.ModelSerializer):
    attendance_count = serializers.SerializerMethodField()
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'surname', 'attendance_count', 'attendances']

    @staticmethod
    def get_attendance_count(obj):
        return obj.attendance.count()

    @staticmethod
    def get_attendances(obj):
        attendances = obj.attendance.all().order_by('-date')
        return AttendanceDisplaySerializer(attendances, many=True).data


class StudentAttendanceGroupSerializer(serializers.ModelSerializer):
    attendance_count = serializers.SerializerMethodField()
    attendances = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'surname', 'attendance_count', 'attendances', ]

    @staticmethod
    def get_attendance_count(obj):
        return obj.attendance.count()

    @staticmethod
    def get_attendances(obj):
        attendances = obj.attendance.all().order_by('-date')
        return AttendanceDisplayGroupSerializer(attendances, many=True).data


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
        fields = ['id', 'name', ]


class AttendanceCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'pair_number', 'status', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d.%m.%Y')
        return representation
