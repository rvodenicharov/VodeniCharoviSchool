from django.urls import path
from .views import CourseCreateView, CourseListView, CourseDetailView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
]