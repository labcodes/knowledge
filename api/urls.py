from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^link/$', views.CreateSlackNewLinkView.as_view(), name="api-link"),
]
