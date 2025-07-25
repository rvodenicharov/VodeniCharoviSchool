from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'bio', 'subjects', 'profile_picture', 'email', 'phone_number']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'bio': 'Биография',
            'subjects': 'Преподавани предмети',
            'profile_picture': 'Профилна снимка',
            'email': 'Имейл',
            'phone_number': 'Телефонен номер',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.FileInput)):
                field.widget.attrs['class'] = 'form-control'
