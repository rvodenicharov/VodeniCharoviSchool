from django.urls import path
from .views import SubjectListView, SubjectDetailView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject_list'),
    path('<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('create/', SubjectCreateView.as_view(), name='subject_create'),
    path('<int:pk>/edit/', SubjectUpdateView.as_view(), name='subject_update'),
    path('<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
]