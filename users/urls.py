from django.urls import path
from . import views

urlpatterns = [
    path('register/',view=views.Register.as_view(),name='registration')
]