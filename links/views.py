from .forms import LinkForm
from .models import Link
from django.views.generic.list import ListView
from django.views.generic import CreateView
from knowledge.settings import LINKS_PER_PAGE
# Create your views here.


class IndexView(ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = LINKS_PER_PAGE
    template_name = 'links/index.html'


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = '/'
    form_class = LinkForm
