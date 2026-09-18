from core.models import ContactInfo, SEOAndContent

c = ContactInfo.load()
c.address = ''
c.save()

s = SEOAndContent.load()
s.meta_title = 'Гвоздев М.Ю. — врач-урогинеколог, хирург | Запись на консультацию'
s.save()

print('address:', repr(ContactInfo.load().address))
print('meta_title:', SEOAndContent.load().meta_title)
