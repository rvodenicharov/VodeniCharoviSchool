from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'start_date', 'end_date', 'price')
    list_filter = ('subject', 'teacher', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'subject__name', 'teacher__first_name', 'teacher__last_name')
    date_hierarchy = 'start_date'
    ordering = ('start_date', 'title')
    raw_id_fields = ('subject', 'teacher')
