import itertools

from django import template
from units.models import Unit_name, Unit_schule, Unit_sprache, Unit_words



register = template.Library()

@register.inclusion_tag('about/menu_items.html', takes_context=True)
def menu_items(context):


    alle_units = Unit_name.objects.all()
    alle_dict = {}
    for schule in Unit_schule.objects.all():
        units_schule = alle_units.filter(schule=schule)
        if units_schule:
            alle_dict[schule] = {}
            for sprache in Unit_sprache.objects.all():
                units_schule_sprache = units_schule.filter(sprache=sprache)
                units_schule_sprache_all = []
                for schule_sprache in units_schule_sprache:  # ist mir egal ob da schon Wörter drinnen sind oder noch nicht, hab keine Zeit mehr!
                    # print(schule_sprache.id)
                    if Unit_words.objects.filter(unit_name__id=schule_sprache.id):
                        units_schule_sprache_all.append(schule_sprache)
                        alle_dict[schule][schule_sprache.sprache] = units_schule_sprache_all

    # print(dict(itertools.islice(alle_dict.items(), 3)))
    return {'items': dict(itertools.islice(alle_dict.items(), 3))}
