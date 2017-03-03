from django.conf.urls import url

from links import views

urlpatterns = [
    url(r'^(?P<tag>\w+)?$', views.ListLinksView.as_view(), name="list-links"),
    url(r'^create/$', views.CreateLinkView.as_view(), name="create_new_link"),
]
