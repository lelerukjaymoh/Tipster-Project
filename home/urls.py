from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^yesterday/$', views.yesterday, name='yesterday'),
    url(r'^$|^today/', views.homepage_today, name='homepage'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^featured/$', views.featured, name='featured'),
]
