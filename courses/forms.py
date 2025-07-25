from django import forms
from django.core.exceptions import ValidationError
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'subject', 'teacher', 'description',
            'price', 'start_date', 'end_date', 'max_students'
        ]
        labels = {
            'title': 'Заглавие',
            'subject': 'Предмет',
            'teacher': 'Преподавател',
            'description': 'Описание',
            'price': 'Цена',
            'start_date': 'Начална дата',
            'end_date': 'Крайна дата',
            'max_students': 'Макс. брой студенти',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError('Крайната дата не може да бъде преди началната дата.')

        return cleaned_data
