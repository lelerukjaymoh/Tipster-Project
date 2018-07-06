from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^before_yesterday/$', views.before_yesterday, name='before_yesterday'),
    url(r'^yesterday/$', views.yesterday, name='yesterday'),
    url(r'^$|^today/', views.homepage_today, name='homepage'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^after_tomorrow/$', views.after_tomorrow, name='after_tomorrow'),
]
