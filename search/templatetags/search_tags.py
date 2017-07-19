from django import template

register = template.Library()

@register.inclusion_tag('search/recipe_search.html', takes_context=True, name='recipe_search')
def recipe_search(context, **kwargs):
    """The recipe search form, to be included in the home page
    """

    # DEFAULT_MESSAGE_LEVELS template var doesn't seem to be available in custom tag
    # so it needs to be passed in by custom template tag in template
    return {
        'messages': context['messages'],
        'form': context['form'],
        'action': context['reverse'],
        'default_message_levels_error': kwargs['default_message_levels_error'],
    }

