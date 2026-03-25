from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'age', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отзыв...'}),
        }