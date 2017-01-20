from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import CreateView, View

from django.conf import settings

from .models import Link
from .forms import LinkForm


class IndexView(ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = settings.LINKS_PER_PAGE
    template_name = 'links/index.html'


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = reverse_lazy('links:index')
    form_class = LinkForm


class CreateSlackNewLinkView(View):

    def post(self, request):

        data = request.POST
        text = data.get('text')
        title, url = text.split(': ')
        Link.objects.create(title=title, url=url)

        return HttpResponse(status=201)
