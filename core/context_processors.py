from .models import ContactInfo, SEOAndContent


def site_globals(request):
    return {
        'contact_info': ContactInfo.load(),
        'seo_info': SEOAndContent.load(),
    }
