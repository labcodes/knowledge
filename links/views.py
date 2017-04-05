from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import Context, Template
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from links.models import Link
from links.forms import LinkForm
from links.serializers import LinkSerializer

from requests.exceptions import ConnectionError

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

from tagging.models import Tag, TaggedItem


class ListLinksView(LoginRequiredMixin, ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


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
