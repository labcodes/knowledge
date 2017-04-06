from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import logout, login
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('links:list-links'))),
]
