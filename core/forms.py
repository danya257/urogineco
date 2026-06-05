from django import forms
from .models import Testimonial, ContactInfo, Hero, AboutDoctor, BlogPost


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


# ============================================================
#  Простые формы для Кабинета (для пожилого пользователя)
#  Крупные поля, понятные подписи, обычные textarea вместо
#  сложного редактора.
# ============================================================

def _cab(widget_cls=forms.TextInput, **attrs):
    attrs.setdefault('class', 'cab-input')
    return widget_cls(attrs=attrs)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'telegram_link', 'whatsapp_link', 'email']
        widgets = {
            'address': _cab(forms.TextInput, placeholder='Город, улица, дом, кабинет'),
            'telegram_link': _cab(forms.TextInput, placeholder='https://t.me/ваш_ник'),
            'whatsapp_link': _cab(forms.TextInput, placeholder='https://wa.me/79991234567'),
            'email': _cab(forms.EmailInput, placeholder='pochta@example.ru'),
        }
        labels = {
            'address': 'Адрес приёма',
            'telegram_link': 'Ссылка на Telegram',
            'whatsapp_link': 'Ссылка на WhatsApp',
            'email': 'Электронная почта',
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['title', 'subtitle', 'description', 'cta_text', 'video_file', 'image']
        widgets = {
            'title': _cab(forms.TextInput, placeholder='Доктор Гвоздев Михаил Юрьевич'),
            'subtitle': _cab(forms.TextInput, placeholder='Врач-урогинеколог · Хирург высшей категории'),
            'description': _cab(forms.Textarea, rows=4, placeholder='Короткое описание под именем'),
            'cta_text': _cab(forms.TextInput, placeholder='Записаться на приём'),
            'video_file': forms.ClearableFileInput(attrs={'class': 'cab-file', 'accept': 'video/*'}),
            'image': forms.ClearableFileInput(attrs={'class': 'cab-file', 'accept': 'image/*'}),
        }
        labels = {
            'title': 'Имя и фамилия (крупный заголовок)',
            'subtitle': 'Подпись под именем',
            'description': 'Короткий текст под именем',
            'cta_text': 'Надпись на кнопке записи',
            'video_file': 'Видео-визитка (.mp4) — врач рассказывает о себе',
            'image': 'Фотография (показывается, пока нет видео)',
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = AboutDoctor
        fields = ['bio', 'experience_years', 'patents', 'awards']
        widgets = {
            'bio': _cab(forms.Textarea, rows=8, placeholder='Расскажите о себе. Каждый новый абзац — с новой строки.'),
            'experience_years': _cab(forms.NumberInput, min=0, max=80),
            'patents': _cab(forms.Textarea, rows=4, placeholder='Патенты и разработки (необязательно)'),
            'awards': _cab(forms.Textarea, rows=4, placeholder='Награды и заслуги (необязательно)'),
        }
        labels = {
            'bio': 'Текст «Обо мне»',
            'experience_years': 'Стаж, лет',
            'patents': 'Патенты и разработки',
            'awards': 'Награды и заслуги',
        }


class DiaryPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'is_published']
        widgets = {
            'title': _cab(forms.TextInput, placeholder='Заголовок записи'),
            'image': forms.ClearableFileInput(attrs={'class': 'cab-file'}),
            'content': _cab(forms.Textarea, rows=12, placeholder='Текст записи. Каждый новый абзац — с новой строки.'),
            'is_published': forms.CheckboxInput(attrs={'class': 'cab-check'}),
        }
        labels = {
            'title': 'Заголовок',
            'image': 'Картинка (необязательно)',
            'content': 'Текст записи',
            'is_published': 'Показывать на сайте',
        }
