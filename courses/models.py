from django.db import models

from teachers.models import Teacher
from subjects.models import Subject

class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заглавие на курса"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Предмет"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        verbose_name="Преподавател"
    )
    description = models.TextField(
        verbose_name="Описание на курса"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена"
    )
    start_date = models.DateField(
        verbose_name="Начална дата"
    )
    end_date = models.DateField(
        verbose_name="Крайна дата"
    )
    max_students = models.PositiveIntegerField(
        default=10,
        verbose_name="Макс. брой студенти"
    )

    class Meta:
        ordering = ['start_date', 'title']
        verbose_name = "Курс"
        verbose_name_plural = "Курсове"

    def __str__(self):
        return self.title