from django.urls import path
from . import views

urlpatterns = [
    path('register/',view=views.Register.as_view(),name='registration'),
    path('verify/',view=views.Verification.as_view(),name='verify'),
    path('login/',view=views.Login.as_view(),name='login'),
    path('logout/',view=views.Logout.as_view(),name='logout'),
]