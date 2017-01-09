from django.conf.urls import url

from links import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
]
