from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import Context, Template
from django.views.generic import CreateView
from django.views.generic.list import ListView

from links.models import Link
from links.forms import LinkForm
from links.serializers import LinkSerializer

from requests.exceptions import ConnectionError

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from tagging.models import Tag, TaggedItem


class ListLinksView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class CreateLinkView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
