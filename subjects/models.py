from django.db import models
from teachers.models import Teacher

class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Име на предмет"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    image = models.ImageField(
        upload_to='subject_images/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"

    def __str__(self):
        return self.name
