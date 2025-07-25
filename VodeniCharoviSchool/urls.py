# VodeniCharoviSchool/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),

    path('register/', core_views.UserRegisterView.as_view(), name='register_user'),
    path('login/', core_views.UserLoginView.as_view(), name='login_user'),
    path('logout/', core_views.UserLogoutView.as_view(), name='logout_user'),

    path('enrollments/', core_views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', core_views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/', core_views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/edit/', core_views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', core_views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),
    path('enrollments/create_from_course/<int:course_pk>/', core_views.enrollment_create_from_course, name='enrollment_create_from_course'),
    path('enrollments/delete_from_course/<int:course_pk>/', core_views.enrollment_delete_from_course, name='enrollment_delete_from_course'),

    path('profile/', core_views.UserProfileView.as_view(), name='user_profile'), # <--- ТОЗИ РЕД Е КЛЮЧОВ!
    path('profile/edit/', core_views.UserProfileUpdateView.as_view(), name='user_profile_update'),

    path('subjects/', include('subjects.urls')),
    path('teachers/', include('teachers.urls')),
    path('courses/', include('courses.urls')),

    path('about/', core_views.AboutView.as_view(), name='about_us'),
    path('contact/', core_views.ContactView.as_view(), name='contact_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)