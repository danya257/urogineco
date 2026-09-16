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
    max_link = models.CharField("Ссылка на MAX", max_length=150, blank=True)
    email = models.EmailField("Email для заявок", blank=True)
    telegram_qr = models.ImageField(
        "QR-код Telegram", upload_to="qr/", blank=True, null=True,
        help_text="Картинка QR для быстрого перехода в канал",
    )
    max_qr = models.ImageField("QR-код MAX", upload_to="qr/", blank=True, null=True)

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
    photo = models.ImageField("Фото", upload_to="procedures/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField("Имя", max_length=100)
    title = models.CharField(
        "Заголовок отзыва", max_length=250, blank=True,
        help_text="Самые яркие слова из отзыва. Если пусто — возьмём начало текста.",
    )
    age = models.PositiveIntegerField("Возраст", blank=True, null=True)
    text = RichTextField("Отзыв", config_name='minimal')
    photo = models.ImageField("Фото", upload_to="testimonials/", blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=False) 
    created_at = models.DateTimeField(auto_now_add=True)  
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']  # новые — сверху

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
    related_event = models.OneToOneField(
        'Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанное мероприятие"
    )
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
    image = models.ImageField("Изображение (анонс)", upload_to="events/", blank=True, null=True)
    video_file = models.FileField(
        "Видео (MP4)", upload_to="events/video/", blank=True,
        help_text="Короткий анонс или запись. Формат .mp4",
    )
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
    city = models.CharField("Город", max_length=100, blank=True)
    address = models.TextField("Адрес")
    metro = models.CharField("Метро / как добраться", max_length=200, blank=True)
    phone = models.CharField("Телефон для записи", max_length=100, blank=True)
    phone_extra = models.CharField("Дополнительный телефон", max_length=100, blank=True)
    contact_person = models.CharField(
        "Контактное лицо", max_length=200, blank=True,
        help_text="Например: администратор Ирина",
    )
    website = models.URLField("Сайт клиники", blank=True)
    map_link = models.URLField("Ссылка на карту (Яндекс.Карты и т.п.)", blank=True)
    order = models.PositiveIntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Адрес клиники"
        verbose_name_plural = "Адреса клиник"
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.address}"

class DoctorLetter(models.Model):
    """Обращение врача к пациенткам на главной."""

    greeting = models.CharField("Приветствие", max_length=200, default="Здравствуйте,")
    intro = models.CharField("Кто я", max_length=200, default="Меня зовут Михаил Юрьевич, врач-урогинеколог.")
    text = RichTextField("Текст обращения", config_name='default', blank=True)
    signature = models.CharField("Подпись", max_length=200, blank=True)
    photo = models.ImageField("Фото врача", upload_to="doctor/", blank=True, null=True)
    banner = models.ImageField(
        "Широкое фото под обращением", upload_to="doctor/", blank=True, null=True,
        help_text="Горизонтальное фото, например из операционной",
    )
    is_visible = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Обращение врача"
        verbose_name_plural = "Обращение врача"

    def __str__(self):
        return "Обращение врача к пациенткам"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroStat(models.Model):
    """Цифры под главным баннером: 30+ лет, 20 000+ операций и т.п."""

    value = models.CharField("Число", max_length=20, help_text="Например: 30+ или 20 000+")
    label = models.CharField("Подпись", max_length=80, help_text="Например: лет хирургического опыта")
    order = models.PositiveIntegerField("Порядок", default=0)
    is_visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Цифра под баннером"
        verbose_name_plural = "Цифры под баннером"
        ordering = ['order']

    def __str__(self):
        return f"{self.value} {self.label}"


class Memo(models.Model):
    """Памятка пациентке: отдельная страница с версией для печати."""

    number = models.CharField("Номер", max_length=4, blank=True, help_text="Например: 01")
    slug = models.SlugField("URL", unique=True)
    title = models.CharField("Название", max_length=200)
    subtitle = models.CharField("Подзаголовок", max_length=250, blank=True)
    body = RichTextField("Текст памятки", config_name='minimal', blank=True)
    file = models.FileField(
        "Файл для скачивания (PDF/DOCX)", upload_to="memos/", blank=True, null=True,
        help_text="Если загружен — на странице появится кнопка «Скачать»",
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_visible = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Памятка пациентке"
        verbose_name_plural = "Памятки пациенткам"
        ordering = ['order', 'number']

    def __str__(self):
        return f"{self.number} {self.title}".strip()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('memo', args=[self.slug])


class Disease(models.Model):
    """Страница заболевания: баннер, видео, разделы текста, памятка и вопросы."""

    slug = models.SlugField("URL", unique=True)
    nav_title = models.CharField("Название в меню", max_length=80)
    title = models.CharField("Заголовок на баннере", max_length=200)
    subtitle = models.CharField("Подзаголовок на баннере", max_length=250, blank=True)
    counter = models.CharField(
        "Счётчик на баннере", max_length=120, blank=True,
        help_text="Например: более 6 500 операций",
    )
    banner = models.ImageField("Фото баннера", upload_to="diseases/", blank=True, null=True)
    icon = models.CharField("Иконка (например, fa-syringe)", max_length=50, blank=True)
    short_description = models.TextField("Краткое описание для карточки", blank=True)

    video_file = models.FileField(
        "Видео (MP4)", upload_to="diseases/video/", blank=True, null=True,
        help_text="Файл проигрывается прямо на странице",
    )
    video_url = models.URLField(
        "Ссылка на видео", blank=True,
        help_text="Если файла нет — ссылка на VK Видео / Rutube / YouTube",
    )
    video_poster = models.ImageField("Обложка видео", upload_to="diseases/", blank=True, null=True)

    lead = RichTextField("Вступление", config_name='minimal', blank=True)
    highlight_title = models.CharField("Заголовок врезки", max_length=200, blank=True)
    highlight_text = RichTextField("Текст врезки", config_name='minimal', blank=True)
    advantages = RichTextField("Преимущества (списком)", config_name='minimal', blank=True)
    benefits = RichTextField("Плюсы операции (списком)", config_name='minimal', blank=True)
    appeal = RichTextField("Обращение к пациенткам", config_name='minimal', blank=True)
    details = RichTextField("Подробнее об операции", config_name='minimal', blank=True)
    about = RichTextField("Подробнее о заболевании", config_name='minimal', blank=True)

    memo = models.ForeignKey(
        Memo, verbose_name="Памятка пациентке", on_delete=models.SET_NULL,
        blank=True, null=True, related_name='diseases',
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_visible = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Страница заболевания"
        verbose_name_plural = "Страницы заболеваний"
        ordering = ['order']

    def __str__(self):
        return self.nav_title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('disease', args=[self.slug])


class Faq(models.Model):
    """Вопрос-ответ: общий список и привязка к странице заболевания."""

    question = models.CharField("Вопрос", max_length=300)
    answer = RichTextField("Ответ", config_name='minimal')
    disease = models.ForeignKey(
        Disease, verbose_name="Относится к заболеванию", on_delete=models.SET_NULL,
        blank=True, null=True, related_name='faqs',
        help_text="Если пусто — вопрос общий",
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопросы и ответы"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class HeroSlide(models.Model):
    """Слайд полноэкранного баннера на главной."""

    KIND_CHOICES = [('video', 'Видео'), ('image', 'Фото / анонс')]

    kind = models.CharField("Тип слайда", max_length=10, choices=KIND_CHOICES, default='image')
    title = models.CharField("Заголовок", max_length=200, blank=True)
    subtitle = models.CharField("Подпись", max_length=300, blank=True)
    image = models.ImageField("Фото (оно же обложка видео)", upload_to="slides/", blank=True, null=True)
    video_file = models.FileField("Видео (MP4)", upload_to="slides/video/", blank=True, null=True)
    button_text = models.CharField("Текст кнопки", max_length=60, blank=True)
    button_url = models.CharField("Ссылка кнопки", max_length=250, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_visible = models.BooleanField("Показывать", default=True)

    class Meta:
        verbose_name = "Слайд баннера"
        verbose_name_plural = "Слайды баннера"
        ordering = ['order']

    def __str__(self):
        return self.title or self.get_kind_display()


# --- 152-ФЗ: заявки с формы ---
from .legal_models import Lead  # noqa: E402,F401
