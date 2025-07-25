from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name="Име"
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия"
    )
    bio = models.TextField(
        verbose_name="Био"
    )
    subjects = models.ManyToManyField(
        'subjects.Subject',
        related_name='teachers',
        verbose_name="Преподавани предмети"
    )
    profile_picture = models.ImageField(
        upload_to='teacher_profiles/',
        blank=True,
        null=True,
        verbose_name="Профилна снимка"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Имейл"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефонен номер"
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Учител"
        verbose_name_plural = "Учители"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"