from django.test import TestCase, Client
from django.urls import reverse
from .models import Course
from subjects.models import Subject
from teachers.models import Teacher
from core.models import Enrollment
from django.contrib.auth import get_user_model
from datetime import date, timedelta

UserModel = get_user_model()

class CourseModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='ИКТ', description='Информационни и комуникационни технологии')
        self.teacher = Teacher.objects.create(first_name='Георги', last_name='Иванов', email='georgi@example.com', bio='ИТ специалист')
        self.course = Course.objects.create(
            title='Въведение в програмирането',
            subject=self.subject,
            teacher=self.teacher,
            description='Курс за начинаещи',
            price=200.00,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            max_students=25
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'Въведение в програмирането')
        self.assertEqual(self.course.subject, self.subject)
        self.assertEqual(self.course.teacher, self.teacher)
        self.assertEqual(self.course.price, 200.00)
        self.assertEqual(str(self.course), 'Въведение в програмирането')

class CourseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.subject = Subject.objects.create(name='Математика', description='Курс по математика')
        self.teacher = Teacher.objects.create(first_name='Иван', last_name='Петров', email='ivan@example.com', bio='Опитен преподавател')
        self.course1 = Course.objects.create(
            title='Алгебра 1',
            subject=self.subject,
            teacher=self.teacher,
            description='Курс по алгебра',
            price=100.00,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            max_students=20
        )
        self.course2 = Course.objects.create(
            title='Геометрия',
            subject=self.subject,
            teacher=self.teacher,
            description='Курс по геометрия',
            price=120.00,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=40),
            max_students=15
        )

    def test_course_list_view(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertContains(response, self.course1.title)
        self.assertContains(response, self.course2.title)
        self.assertQuerySetEqual(response.context['courses'], [self.course1, self.course2], ordered=False)

    def test_course_detail_view_not_enrolled(self):
        response = self.client.get(reverse('course_detail', args=[self.course1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, self.course1.title)
        self.assertNotContains(response, 'Запиши се за курса')
        self.assertNotContains(response, 'Отпиши се от курса')

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('course_detail', args=[self.course1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, 'Запиши се за курса')
        self.assertNotContains(response, 'Отпиши се от курса')

    def test_course_detail_view_enrolled(self):
        self.client.login(username='testuser', password='password123')
        Enrollment.objects.create(student=self.user, course=self.course1)
        response = self.client.get(reverse('course_detail', args=[self.course1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertContains(response, self.course1.title)
        self.assertContains(response, 'Отпиши се от курса')
        self.assertNotContains(response, 'Запиши се за курса')
