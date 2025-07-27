from django.db.models import Q
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course
from .forms import CourseForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.models import Enrollment
from subjects.models import Subject
from teachers.models import Teacher

class CourseCreateView(PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.add_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Създаване на нов курс'
        return context

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    ordering = ['start_date', 'title']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        subject_id = self.request.GET.get('subject')
        teacher_id = self.request.GET.get('teacher')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(subject__name__icontains=query) |
                Q(teacher__first_name__icontains=query) |
                Q(teacher__last_name__icontains=query)
            ).distinct()

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['subjects'] = Subject.objects.all().order_by('name')
        context['teachers'] = Teacher.objects.all().order_by('last_name', 'first_name')
        context['selected_subject'] = self.request.GET.get('subject', '')
        context['selected_teacher'] = self.request.GET.get('teacher', '')
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        is_enrolled = False
        enrollment_obj = None
        if self.request.user.is_authenticated:
            try:
                enrollment_obj = Enrollment.objects.get(student=self.request.user, course=course)
                is_enrolled = True
            except Enrollment.DoesNotExist:
                is_enrolled = False

        context['is_enrolled'] = is_enrolled
        context['enrollment_obj'] = enrollment_obj

        return context

class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.change_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Редактиране на курс: {self.object.title}'
        return context

class CourseDeleteView(PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses.delete_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object()
        return context
