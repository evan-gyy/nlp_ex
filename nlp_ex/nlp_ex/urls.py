from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import view, testdb, cloud, extract
from show_pages import views

urlpatterns = [
    path('index/', views.index),
    path('text_titles/', views.text_title),
    path('text_content/', views.text_content),
    url(r'^hello$', view.hello),
    url(r'^testdb$', testdb.testdb),
    url(r'^cloud$', cloud.get_cloud),
    url(r'^summary$', extract.summary),
]
