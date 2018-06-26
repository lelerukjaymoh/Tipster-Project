from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$|^today', views.homepage, name='homepage'),
    url(r'^yesterday$', views.homepage, name='yesterday'),
    url(r'^tomorrow$', views.homepage, name='tomorrow'),
]
