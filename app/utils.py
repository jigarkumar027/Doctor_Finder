from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sendmaildoc(subject,template,to,context):
    subject = 'Doctor Varification'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailpat(subject,template,to,context):
    subject = 'Patient Varification'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailpha(subject,template,to,context):
    subject = 'Pharmacy Varification'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailappo(subject,template,to,context):
    subject = 'Booking Appointment'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmailpre(subject,template,to,context):
    subject = 'Appointment Status'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendmail(subject,template,to,context):
    subject = 'Email Verification'
    template_str = 'app/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'doctorfinder2021@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)