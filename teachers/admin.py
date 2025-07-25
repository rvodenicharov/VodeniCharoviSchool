from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'get_subjects')
    search_fields = ('first_name', 'last_name', 'email', 'bio')
    list_filter = ('subjects',)
    ordering = ('last_name', 'first_name')

    def get_subjects(self, obj):
        return ", ".join([s.name for s in obj.subjects.all()])
    get_subjects.short_description = 'Преподава предмети'
