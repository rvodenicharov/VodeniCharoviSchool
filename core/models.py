from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Course

UserModel = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        verbose_name="Потребител"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Био"
    )
    profile_picture = models.ImageField(
        upload_to='user_profiles/',
        blank=True,
        null=True,
        verbose_name="Профилна снимка"
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефонен номер"
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255, blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Профил"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профил на {self.user.username}"


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Enrollment(models.Model):
    student = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)


    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Записване"
        verbose_name_plural = "Записвания"

    def __str__(self):
        return f"{self.student.username} записан в {self.course.title}"