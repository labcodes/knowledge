from django.urls import reverse_lazy
from django.views.generic.list import ListView

from django.views.generic import CreateView, View

from django.conf import settings

from .models import Link
from .forms import LinkForm

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class IndexView(ListView):
    model = Link
    context_object_name = 'links'
    paginate_by = settings.LINKS_PER_PAGE
    template_name = 'links/index.html'


class CreateLinkView(CreateView):
    template_name = 'links/create-link-form.html'
    success_url = reverse_lazy('links:index')
    form_class = LinkForm


class CreateSlackNewLinkView(APIView):

    def post(self, request):
        text = request.POST.get('text')

        try:
            Link.objects.create_from_slack(text)
        except ValueError:
            return Response({
                'text': 'Your Link is not valid.\nPlease check the syntax: title: url'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=201)
