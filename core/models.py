from django.db import models
from ckeditor.fields import RichTextField


class SEOAndContent(models.Model):
    """Главная SEO-запись (только одна)"""
    meta_title = models.CharField(
        "Title для SEO",
        max_length=100,
        default="Доктор Гвоздев М.Ю. | Урогинеколог в Москве"
    )
    meta_description = models.CharField(
        "Description для SEO",
        max_length=200,
        default="Врач-урогинеколог высшей категории. Операции при недержании, пролапсе, свищах. Автор патентованной методики."
    )
    og_image = models.ImageField(
        "OG-изображение (для соцсетей)",
        upload_to="seo/",
        blank=True,
        null=True,
        help_text="Рекомендуется 1200×630 px"
    )

    class Meta:
        verbose_name = "SEO и контент"
        verbose_name_plural = "SEO и контент"

    def __str__(self):
        return "Настройки SEO"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Hero(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    subtitle = models.CharField("Подзаголовок", max_length=300)
    description = RichTextField("Описание", config_name='minimal')
    image = models.ImageField("Фото врача (700×700)", upload_to="heroes/", blank=True, null=True)
    cta_text = models.CharField("Текст кнопки записи", max_length=50, default="Записаться на приём")
    video_file = models.FileField(
    "Видео (MP4, до 50 МБ)",
    upload_to="hero_videos/",
    blank=True,
    help_text="Поддерживаемый формат: .mp4. Рекомендуется сжать видео до 30–50 МБ."
)

    class Meta:
        verbose_name = "Главная секция"
        verbose_name_plural = "Главная секция"

    def __str__(self):
        return "Настройки главного блока"


class Direction(models.Model):
    title = models.CharField("Название направления", max_length=150)
    description = models.CharField("Краткое описание", max_length=200)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Направление помощи"
        verbose_name_plural = "Направления помощи"
        ordering = ['order']

    def __str__(self):
        return self.title


class WorkExample(models.Model):
    title = models.CharField("Название кейса (для админа)", max_length=200)
    public_title = models.CharField("Заголовок на сайте", max_length=200, default="Операция")
    description = RichTextField("Описание (на сайте, до раскрытия)", config_name='minimal')
    image_original = models.ImageField(
        "Фото (оригинал)",
        upload_to="work_examples/",
        help_text="Фото будет размыто на сайте до клика"
    )
    is_published = models.BooleanField("Показывать на сайте", default=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Пример работы"
        verbose_name_plural = "Примеры работ"
        ordering = ['order']

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    description = RichTextField("Описание", config_name='minimal')
    badge_text = models.CharField("Текст бейджа", max_length=100, blank=True)
    badge_color = models.CharField(
        "Цвет бейджа",
        max_length=20,
        choices=[('gold', 'Золотой'), ('pink', 'Розовый'), ('blue', 'Синий')],
        default='gold'
    )
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Достижение / Факт"
        verbose_name_plural = "Достижения и факты"
        ordering = ['order']

    def __str__(self):
        return self.title


class EducationItem(models.Model):
    year = models.CharField("Год", max_length=4)
    title = models.CharField("Название", max_length=250)
    description = RichTextField("Описание", config_name='minimal')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Этап образования"
        verbose_name_plural = "Образование"
        ordering = ['order']

    def __str__(self):
        return f"{self.year} — {self.title}"


class ContactInfo(models.Model):
    address = models.CharField("Адрес приёма", max_length=250, blank=True)
    telegram_link = models.CharField("Ссылка на Telegram", max_length=150, blank=True)
    whatsapp_link = models.CharField("Ссылка на WhatsApp", max_length=150, blank=True)
    email = models.EmailField("Email для заявок", blank=True)

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return "Контакты (только 1 запись)"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# --- Новые модели для дополнительных разделов ---
class Procedure(models.Model):
    title = models.CharField("Название операции", max_length=200)
    description = RichTextField("Описание", config_name='minimal')
    icon = models.CharField("Иконка (например, fa-syringe)", max_length=50, blank=True)
    photo = models.ImageField("Фото", upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveIntegerField("Возраст", blank=True, null=True)
    text = RichTextField("Отзыв", config_name='minimal')
    photo = models.ImageField("Фото", upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['order']

    def __str__(self):
        return f"Отзыв от {self.name}"


class BlogPost(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("URL", unique=True, blank=True)
    content = RichTextField("Контент", config_name='default')
    image = models.ImageField("Изображение", upload_to="blog/", blank=True, null=True)
    published_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Дневник врача"
        verbose_name_plural = "Дневник врача"
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField("Название события", max_length=200)
    date = models.DateField("Дата")
    location = models.CharField("Место", max_length=200)
    description = RichTextField("Описание", config_name='minimal', blank=True)
    link = models.URLField("Ссылка", blank=True, help_text="Ссылка на мероприятие")
    image = models.ImageField("Изображение", upload_to="events/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class AboutDoctor(models.Model):
    bio = RichTextField("Биография", config_name='default')
    experience_years = models.PositiveIntegerField("Стаж (лет)", default=18)
    patents = RichTextField("Патенты и разработки", config_name='minimal', blank=True)
    awards = RichTextField("Награды и заслуги", config_name='minimal', blank=True)

    class Meta:
        verbose_name = "О враче"
        verbose_name_plural = "О враче"

    def __str__(self):
        return "Информация о докторе Гвоздеве М.Ю."

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class UsefulInfo(models.Model):
    prep_consultation = RichTextField("Подготовка к консультации", config_name='minimal', blank=True)
    prep_surgery = RichTextField("Подготовка к операции", config_name='minimal', blank=True)
    anesthesia_info = RichTextField("Обезболивание при операции", config_name='minimal', blank=True)
    postop_period = RichTextField("Послеоперационный период", config_name='minimal', blank=True)

    class Meta:
        verbose_name = "Важное пациенткам"
        verbose_name_plural = "Важное пациенткам"

    def __str__(self):
        return "Важная информация для пациенток"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class ClinicLocation(models.Model):
    name = models.CharField("Название клиники", max_length=200)
    address = models.TextField("Адрес")
    map_link = models.URLField("Ссылка на карту (Google Maps и т.п.)", blank=True)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Адрес клиники"
        verbose_name_plural = "Адреса клиник"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.address}"  