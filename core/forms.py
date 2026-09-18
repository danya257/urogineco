from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    """Форма отзыва: обязательный чекбокс согласия на публикацию + обработку ПД (152-ФЗ)."""

    consent = forms.BooleanField(
        label='Согласен(на) на обработку персональных данных и публикацию отзыва',
        required=True,
        error_messages={'required': 'Без согласия на обработку персональных данных отзыв отправить нельзя.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
    )

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
                'min': 18,
                'max': 110,
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Расскажите, с чем обращались и как прошло лечение',
            }),
        }
        labels = {
            'name': 'Имя',
            'age': 'Возраст',
            'text': 'Ваш отзыв',
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and not 18 <= age <= 110:
            raise forms.ValidationError('Укажите возраст от 18 до 110 лет или оставьте поле пустым.')
        return age

    def clean_text(self):
        text = (self.cleaned_data.get('text') or '').strip()
        if len(text) < 10:
            raise forms.ValidationError('Отзыв слишком короткий.')
        return text
