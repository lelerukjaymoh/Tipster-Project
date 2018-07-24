from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^yesterday/$', views.yesterday, name='yesterday'),
    url(r'^$|^today/', views.homepage_today, name='homepage'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^featured/$', views.featured, name='featured'),
    url(r'game_details/(?P<pk>[{\w+}* -{\w+}*]+)', views.game_details, name="game_details"),
]
