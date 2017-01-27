from django.conf.urls import url
from django.contrib.auth.views import logout

from links import views

urlpatterns = [
    url(r'^$', views.ListLinksView.as_view(), name="list-links"),
    url(r'^create/$', views.CreateLinkView.as_view(), name="create_new_link"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^accounts/logout/$', logout, {'next_page': 'links:list-links'}, name="logout"),
]
