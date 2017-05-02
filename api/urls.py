from django.conf.urls import url, include

from api import views

urlpatterns = [
    url(r'^link/$', views.CreateSlackNewLinkView.as_view(), name="api-link"),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
