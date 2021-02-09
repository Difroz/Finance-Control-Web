from django.views.generic import TemplateView, ListView, View
from .logic import get_balans

class Index(TemplateView):
    template_name = 'statistics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = get_balans(self.request.user)
        print(context['balance'])
        return context

