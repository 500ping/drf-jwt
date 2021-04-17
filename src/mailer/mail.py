from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site

def resgister_confirm(user, token):
    text_content = render_to_string('mail/register-confirm.txt', context={
        'username': user.user_name,
        'url': f'{Site.objects.get_current().domain}api/user/email-verification/{token}'
    })
    html_content = render_to_string('mail/register-confirm.html', context={
        'username': user.user_name,
        'url': f'{Site.objects.get_current().domain}api/user/email-verification/{token}'
    })

    subject, from_email, to = 'Email Verification', 'from@example.com', user.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
