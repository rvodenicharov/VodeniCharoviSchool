from django.urls import path, include
from .views import (
    index, UserRegisterView, UserLoginView, UserLogoutView,
    EnrollmentListView, EnrollmentCreateView, EnrollmentDetailView,
    EnrollmentUpdateView, EnrollmentDeleteView,
    enrollment_create_from_course, enrollment_delete_from_course,
    UserProfileView, UserProfileUpdateView,
    AboutView, ContactView
)

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='login_user'),
    path('logout/', UserLogoutView.as_view(), name='logout_user'),
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/edit/', EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
    path('enrollments/create_from_course/<int:course_pk>/', enrollment_create_from_course, name='enrollment_create_from_course'),
    path('enrollments/delete_from_course/<int:course_pk>/', enrollment_delete_from_course, name='enrollment_delete_from_course'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('subjects/', include('subjects.urls')),
    path('teachers/', include('teachers.urls')),
    path('courses/', include('courses.urls')),
    path('about/', AboutView.as_view(), name='about_us'),
    path('contact/', ContactView.as_view(), name='contact_us'),
]
