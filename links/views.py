from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from links.models import Link
from links.forms import LinkForm

from requests.exceptions import ConnectionError
# from tagging.models import Tag


class ListLinksView(LoginRequiredMixin, ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = settings.LINKS_PER_PAGE
    template_name = 'links/index.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['tags'] = Link.tags.split(', ')
        context.update(kwargs)
        return super(ListLinksView, self).get_context_data(**context)


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = reverse_lazy('links:list-links')
    form_class = LinkForm

    def form_valid(self, form):
        try:
            form.save(author=self.request.user)
        except ConnectionError:
            messages.error(self.request, "Your Link is not valid. Please check your url.")

        return redirect(self.success_url)
