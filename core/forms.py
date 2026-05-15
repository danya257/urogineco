from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'age', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например, Анна',
                'maxlength': 100,
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Возраст (необязательно)',
                'min': 0,
                'max': 120,
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Поделитесь вашим опытом...',
            }),
        }
        labels = {
            'name': 'Имя',
            'age': 'Возраст',
            'text': 'Ваш отзыв',
        }
