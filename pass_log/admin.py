from django.contrib import admin
from .models import Group, Student, Attendance


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'curator', 'captain')  # Поля, отображаемые в списке
    search_fields = ('name',)  # Поля, по которым можно искать
    ordering = ('name',)  # Поля для сортировки


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'group')  # Поля, отображаемые в списке
    search_fields = ('name', 'surname')  # Поля, по которым можно искать
    ordering = ('name', 'surname', 'group')  # Поля для сортировки


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'pair_number', 'status')  # Поля, отображаемые в списке
    list_filter = ('date', 'status')  # Фильтры по полям
    search_fields = ('student__name', 'student__surname')  # Поиск по имени и фамилии студента
