from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EnrollmentForm, UserProfileForm
from .models import Enrollment, Profile
from courses.models import Course

def index(request):
    return render(request, 'core/index.html', {
        'page_title': 'Начална страница на Школа Воденичарови',
        'welcome_message': 'Добре дошли в Школа Воденичарови! Разгледайте нашите предмети и преподаватели.',
    })

class UserRegisterView(CreateView):
    template_name = 'core/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login_user')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Успешна регистрация! Моля, влезте.')
        return response

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
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(
            student=self.request.user
        ).order_by('-enrollment_date')
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = 'core/user_profile_form.html'
    success_url = reverse_lazy('user_profile')
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактиране на профил'
        return context

@login_required
def enrollment_create_from_course(request, course_pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_pk)
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, f'Вече сте записани за курса "{course.title}".')
        elif course.max_students and course.enrollments.count() >= course.max_students:
            messages.error(request, f'Курсът "{course.title}" е пълен.')
        else:
            Enrollment.objects.create(student=request.user, course=course)
            messages.success(request, f'Успешно се записахте за курса "{course.title}".')
        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')

@login_required
def enrollment_delete_from_course(request, course_pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_pk)
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            enrollment.delete()
            messages.success(request, f'Успешно се отписахте от курса "{course.title}".')
        except Enrollment.DoesNotExist:
            messages.error(request, f'Не сте записани за курса "{course.title}".')
        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')

class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'core/enrollment_list.html'
    context_object_name = 'enrollments'
    ordering = ['-enrollment_date']

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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Записване за курс'
        return context

class EnrollmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Enrollment
    template_name = 'core/enrollment_detail.html'
    context_object_name = 'enrollment'

    def test_func(self):
        enrollment = self.get_object()
        return self.request.user.is_staff or enrollment.student == self.request.user

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

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'
