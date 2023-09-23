from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', views.MyLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout, name='logout')
]
