from .forms import LinkForm
from .models import Link
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import CreateView, View
from knowledge.settings import LINKS_PER_PAGE
from django.urls import reverse_lazy

# Create your views here.


class IndexView(ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = LINKS_PER_PAGE
    template_name = 'links/index.html'


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = reverse_lazy('links:index')
    form_class = LinkForm


class CreateSlackNewLinkView(View):

    def post(self, request):

        data = request.POST

        text = data.get('text')

        separation_between_title_and_url = text.find(':')
        url_position = text.find('http')

        link_title = text[:separation_between_title_and_url]
        link_url = text[url_position:]

        new_link = Link(title=link_title, url=link_url)
        new_link.save()

        return HttpResponse(status=200)
