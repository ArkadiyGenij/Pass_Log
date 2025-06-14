from rest_framework.permissions import BasePermission


class IsCuratorOrCaptainOfStudentGroup(BasePermission):
    """
    Доступ к куратору или старосте группы студента
    """

    def has_permission(self, request, view):
        if request.method in ('DELETE', 'PUT', 'PATCH'):
            return True

        if request.method == 'POST':
            student_id = request.data.get('student')
            if not student_id:
                return False

            from pass_log.models import Student
            try:
                student = Student.objects.get(id=student_id)
                group = student.group
                return request.user == group.curator or request.user == group.captain
            except Student.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        group = obj.student.group
        return request.user == group.curator or request.user == group.captain
