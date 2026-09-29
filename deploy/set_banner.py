import os
from django.core.files import File
from core.models import Disease

src = os.path.join(os.environ.get('TZ_MEDIA', ''), 'image1.png')
d = Disease.objects.filter(slug='nederzhanie-mochi').first()
if d and not d.banner and os.path.exists(src):
    with open(src, 'rb') as f:
        d.banner.save('nederzhanie.png', File(f), save=True)
print('banner:', d.banner.url if d and d.banner else None)
