from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from urllib.parse import urlencode

from common.utils import cleanup_ingredients

class RecipeSearchForm(forms.Form):
    """Simple search form config, for validating against
    """

    def __init__(self, *args, **kwargs):
        super(RecipeSearchForm, self).__init__(*args, **kwargs)

    ingredients = forms.CharField(label='Ingredients', max_length=2000, required=True)

    def process_post(self, request, context):
        """Process the posted recipe search form

        Params:
            request object,
            context, which must contain:
                page_title (page's title)
                reverse (originating page's view name, to return to in the event of errors or no results)
                template (originating page's template)

        Pre-processes form, returning to the originating page (rendering its template) with form errors
        if not valid, or if valid then passing on to further processing by search app (which will do the
        actual searching)

        This is all necessary so that originating pages can be displayed with errors, and successful GET
        requests to search can be bookmarked by users

        Returns:
            HttpResponse obj
        """

        # Return to originating page with the original context and form object for
        # displaying the form validation errors
        if not self.is_valid():
            context['form'] = self
            return render(request, context['template'], context)

        query_dict = {
            'ingredients': cleanup_ingredients(self.cleaned_data.get('ingredients')),
            'reverse': context['reverse'],
            'page_title': context['page_title']
        }
        query_str = urlencode(query_dict)
        search_url = reverse('search:process_recipe_search') + '?' + query_str
        return HttpResponseRedirect(search_url)

