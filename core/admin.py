# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Enrollment

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'get_phone_number', 'get_address'
    )

    def get_phone_number(self, obj):
        return obj.profile.phone_number
    get_phone_number.short_description = 'Телефонен номер'

    def get_address(self, obj):
        return obj.profile.address
    get_address.short_description = 'Адрес'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'completed')
    list_filter = ('completed', 'course', 'student')
    search_fields = ('student__username', 'course__title')
    date_hierarchy = 'enrollment_date'
    ordering = ('-enrollment_date',)
