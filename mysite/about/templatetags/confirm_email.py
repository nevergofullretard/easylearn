from django import template
from emails.models import Confirm_email

register = template.Library()

@register.inclusion_tag('about/confirm_email.html', takes_context=True)
def confirm_email(context):
    user = context.get('user')
    return {'confirm_email': Confirm_email.objects.filter(user=user)}
