# VodeniCharoviSchool/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),

    path('register/', core_views.UserRegisterView.as_view(), name='register_user'),
    path('login/', core_views.UserLoginView.as_view(), name='login_user'),
    path('logout/', core_views.UserLogoutView.as_view(), name='logout_user'),

    path('dashboard/', core_views.DashboardView.as_view(), name='dashboard'),

    path('profile/', core_views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', core_views.UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('enrollments/', core_views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', core_views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/', core_views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/edit/', core_views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', core_views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    path('courses/<int:course_pk>/enroll/', core_views.enroll_in_course, name='enroll_in_course'), # <--- НОВ
    path('enrollments/<int:enrollment_pk>/unenroll/', core_views.unenroll_from_course, name='unenroll_from_course'), # <--- НОВ

    path('subjects/', include('subjects.urls')),
    path('teachers/', include('teachers.urls')),
    path('courses/', include('courses.urls')),

    path('about/', core_views.about_us, name='about_us'),
    path('contact/', core_views.contact_us, name='contact_us'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)