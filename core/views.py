from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import UserRegisterForm, EnrollmentForm, UserProfileForm
from .models import Profile, Enrollment
from subjects.models import Subject
from teachers.models import Teacher
from courses.models import Course
from django.db import IntegrityError, transaction

def index(request):
    return render(request, 'core/index.html')

def about_us(request):
    return render(request, 'core/about.html')

def contact_us(request):
    return render(request, 'core/contact.html')

class UserRegisterView(CreateView):
    template_name = 'core/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login_user')

    def form_valid(self, form):
        messages.success(self.request, 'Успешна регистрация! Моля, влезте.')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'core/user_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['enrollments'] = Enrollment.objects.filter(student=user).select_related('course').order_by('-enrollment_date')
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'core/user_profile_form.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактиране на профил'
        return context

class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'core/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Enrollment.objects.all().select_related('student', 'course', 'course__subject', 'course__teacher').order_by('-enrollment_date')
        return Enrollment.objects.filter(student=self.request.user).select_related('course', 'course__subject', 'course__teacher').order_by('-enrollment_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class EnrollmentDetailView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'core/enrollment_detail.html'
    context_object_name = 'enrollment'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student=self.request.user)

class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'core/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.enrollment_date = timezone.now()
        messages.success(self.request, 'Успешно се записахте за курса!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Записване за нов курс'
        return context

class EnrollmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'core/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')
    permission_required = 'core.change_enrollment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Редактиране на записване за: {self.object.course.title}'
        return context

class EnrollmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'core/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment_list')
    permission_required = 'core.delete_enrollment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollment'] = self.get_object()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = user.profile if hasattr(user, 'profile') else None
        context['enrolled_courses'] = Enrollment.objects.filter(student=user).select_related('course').order_by('-enrollment_date')
        return context

@login_required
@require_POST
def enroll_in_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    try:
        with transaction.atomic():
            Enrollment.objects.create(student=request.user, course=course, enrollment_date=timezone.now())
            messages.success(request, f'Успешно се записахте за курса "{course.title}"!')
    except IntegrityError:
        messages.warning(request, f'Вече сте записани за курса "{course.title}".')
    return redirect('course_detail', pk=course_pk)

@login_required
@require_POST
def unenroll_from_course(request, enrollment_pk):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_pk, student=request.user)
    course_title = enrollment.course.title
    enrollment.delete()
    messages.success(request, f'Успешно се отписахте от курса "{course_title}".')
    return redirect('course_detail', pk=enrollment.course.pk)
