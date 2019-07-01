from datetime import date
from django.utils import timezone


from django import template
from blog.models import Post
register = template.Library()

@register.inclusion_tag('about/linked_in_post.html', takes_context=True)
def linked_in_post(context):
    user = context.get('user')
    qry = Post.objects.filter(linked=user).order_by('-date_posted')
    not_viewed = []
    for post in qry:
        viewed = post.viewed
        if viewed:
            if str(user.id) not in viewed.split(','):
                not_viewed.append(post)
        else:
            not_viewed.append(post)

    limited = not_viewed[:4]
    all_not_viewed = []

    if len(not_viewed) >= 5:
        all_not_viewed = not_viewed[4:]
    anzahl = len(not_viewed)


    return {'posts': limited, 'all_posts': all_not_viewed, 'anzahl': anzahl}