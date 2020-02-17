from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import view, testdb, cloud, extract
from crawler import sina_news
from user import login, register
from show_pages import views

urlpatterns = [
    path('index/', views.index),
    path('text_titles/', views.text_title),
    path('text_content/', views.text_content),
    path('spread_wci/', views.spread_wci),
    url(r'^text_title$', views.text_title),
    url(r'^$',views.index),
    url(r'^hello$', view.hello),
    url(r'^testdb$', testdb.testdb),
    url(r'^cloud$', cloud.get_cloud),
    url(r'^summary$', extract.summary),
    url(r'^sina_news$', sina_news.get_pages),
    url(r'^login$', login.login),
    url(r'^logout$', login.logout),
    url(r'^register$', register.register),

]
