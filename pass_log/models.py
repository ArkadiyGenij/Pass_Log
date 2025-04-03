from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="название группы")
    curator = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                verbose_name='куратор', related_name="curator_groups")
    captain = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                verbose_name='староста', related_name="captain_groups")

    # curator =

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name="имя студента")
    surname = models.CharField(max_length=30, verbose_name="фамилия студента")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="students",
                              verbose_name="группа")

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"

    def __str__(self):
        return self.name + " " + self.surname


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Присутствовал'),
        ('absent_excused', 'Отсутствовал с уважительной причиной'),
        ('absent_unexcused', 'Отсутствовал без уважительной причины'),
        ('unknown', 'Неизвестно'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name="attendance",
                                verbose_name="студент")
    date = models.DateField(verbose_name="дата")
    pair_number = models.PositiveIntegerField(verbose_name="номер пары")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="причина пропуска")

    class Meta:
        unique_together = ('student', 'date', 'pair_number')
        verbose_name = "посещаемости"
        verbose_name_plural = "посещаемости"

    def __str__(self):
        return f"{self.student.name} - {self.date} - пара {self.pair_number}"
