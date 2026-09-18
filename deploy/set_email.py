from core.models import ContactInfo

c = ContactInfo.load()
c.email = 'dr-gvozdev@mail.ru'
# Заглушки из populate ведут на чужие аккаунты — убираем, пока нет настоящих
if c.telegram_link == 'https://t.me/gvozdev_md':
    c.telegram_link = ''
if c.whatsapp_link == 'https://wa.me/79991234567':
    c.whatsapp_link = ''
c.save()
print('email:', c.email, '| tg:', repr(c.telegram_link), '| wa:', repr(c.whatsapp_link), '| address:', c.address)
