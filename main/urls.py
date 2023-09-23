from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('faculty-house', views.faculty_house, name='faculty_house'),
    path('ferris-booth', views.ferris_booth, name='ferris_booth'),
    path('jj-place', views.jj_place, name='jj_place'),
    path('mike-sub', views.mike_sub, name='mike_sub')
]
