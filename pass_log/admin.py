from io import BytesIO

import openpyxl
import pandas as pd
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from .forms import ExcelImportForm
from .models import Group, Student, Attendance


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'curator', 'captain')  # Поля, отображаемые в списке
    search_fields = ('name',)  # Поля, по которым можно искать
    ordering = ('name',)  # Поля для сортировки


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    change_list_template = "admin/student_change_list.html"

    list_display = ('id', 'name', 'surname', 'group')  # Поля, отображаемые в списке
    search_fields = ('name', 'surname')  # Поля, по которым можно искать
    ordering = ('name', 'surname', 'group')  # Поля для сортировки

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-excel/", self.import_excel),
            path('download-template/', self.admin_site.admin_view(self.download_template),
                 name='download_student_template'),
        ]
        return my_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                df = pd.read_excel(request.FILES['excel_file'])

                for _, row in df.iterrows():
                    group_name = row['группа']
                    group, created = Group.objects.get_or_create(name=group_name)

                    Student.objects.create(
                        name=row['имя'],
                        surname=row['фамилия'],
                        group=group,
                    )

                self.message_user(request, "Импорт завершён.")
                return redirect("..")

        else:
            form = ExcelImportForm()

        context = {
            "form": form,
            "title": "Импорт студентов из Excel"
        }

        return render(request, "admin/excel_form.html", context)

    def download_template(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students template"

        ws.append(["имя", "фамилия", "группа"])

        output = BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=student_template.xlsx'
        return response



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'pair_number', 'status')  # Поля, отображаемые в списке
    list_filter = ('date', 'status')  # Фильтры по полям
    search_fields = ('student__name', 'student__surname')  # Поиск по имени и фамилии студента
