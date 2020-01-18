from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView


class GenericClassBasedView(TemplateView):
    """Generic Class-Based View (gCBV)"""

    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        """Return the context."""
        context = super().get_context_data(**kwargs)
        context['title'] = "Welcome to the main view"
        return context


class ClassBasedView(View):
    """Class-Based View (CBV)"""

    def get(self, request, *args, **kwargs):
        template_name = kwargs['template']
        # This data dict will be added to the template context
        data = {}
        data['title'] = "Welcome to the '" + \
            kwargs['template'] + "' view (Class-Based View)"
        return render(request, template_name, data)

    def post(self, request):
        # We don't handle POST requests
        pass
