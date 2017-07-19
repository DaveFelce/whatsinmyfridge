from django.core.urlresolvers import reverse
from django.views import View
from django.shortcuts import render
from django.contrib.messages import get_messages
from search.forms import RecipeSearchForm

class Home(View):
    """Home page class-based view

    Args:
        View (:obj:Django View base class, required)

    """

    def common_context(self):
        """Common data for the context var: both get() and post() will
        require these
        """

        context = {
            'page_title': "What's in my Fridge",
            'reverse': reverse("home:index"), # So we can get back here if things go wrong
        }
        return context

    def get(self, request):
        """get http method: search form will be empty
        """
        context = self.common_context()
        context.update({
            'form': RecipeSearchForm(),
            'messages': get_messages(request),
        })
        return render(request, 'home/index.html', context)

    def post(self, request):
        """post http method: search form will be submitted
        """
        form = RecipeSearchForm(request.POST)

        context = self.common_context()
        context.update({
            'template': 'home/index.html',
        })
        # Process the form and return the results
        return form.process_post(request, context)
