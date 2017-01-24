from django.conf.urls import url

from links import views

urlpatterns = [
    url(r'^$', views.ListLinksView.as_view(), name="list-links"),
    url(r'^create-new-link/$', views.CreateLinkView.as_view(), name="create_new_link"),
    url(r'^api/link/$', views.CreateSlackNewLinkView.as_view(), name="api-link"),
]
