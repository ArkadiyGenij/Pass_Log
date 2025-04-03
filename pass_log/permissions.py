from rest_framework import permissions

from pass_log.models import Student


class IsCuratorOrCaptainOfStudentGroup(permissions.BasePermission):
    """
    Разрешение для куратора или старосты добавлять пропуски только для студентов своей группы.
    """

    def has_permission(self, request, view):
        # Получаем пользователя из запроса
        user = request.user

        # Получаем студента, для которого создается пропуск
        student_id = request.data.get("student")  # Предполагаем, что в запросе есть идентификатор студента
        student = Student.objects.get(id=student_id)

        # Получаем группу этого студента
        group = student.group

        # Проверяем, является ли пользователь старостой или куратором этой группы
        if user == group.curator or user == group.captain:
            return True

        return False
