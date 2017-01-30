from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import logout, login
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('links:list-links'))),
    url(r'^accounts/login/$', login, {'template_name': 'core/login.html'}, name="login"),
    url(r'^accounts/logout/$', logout, {'next_page': 'core:login'}, name="logout"),
]
