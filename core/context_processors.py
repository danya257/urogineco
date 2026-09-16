from .models import ContactInfo, SEOAndContent, Disease


def site_globals(request):
    return {
        'contact_info': ContactInfo.load(),
        'seo_info': SEOAndContent.load(),
        'nav_diseases': Disease.objects.filter(is_visible=True),
    }
