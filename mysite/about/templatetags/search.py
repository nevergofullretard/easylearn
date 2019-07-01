from django import template
from units.models import Unit_words, Unit_name, Unit_schule, Unit_sprache
from blog.models import Post
from django.contrib.auth.models import User
register = template.Library()

@register.inclusion_tag('about/search.html', takes_context=True)
def search(context):
    words = Unit_words.objects.all()
    units = Unit_name.objects.all()
    schulen = Unit_schule.objects.all()
    sprachen = Unit_sprache.objects.all()
    posts = Post.objects.all()
    users = User.objects.all()
    all = []

    [all.append(word) for word in users]
    [all.append(word) for word in schulen]
    [all.extend((word.sprache_lang, word)) for word in sprachen]
    [all.append(word) for word in units]
    [all.extend((word, word.deutsch)) for word in words]
    [all.append(word) for word in posts]

    # for word, unit, schule, sprache, post, user in zip(words, units, schulen, sprachen, posts, users):
    #     all.append(word)
    #     all.append(unit)
    #     all.append(sprache)
    #     all.append(schule)
    #     all.append(post)
    #     all.append(user)
    # print(words)

    return {'words': all}