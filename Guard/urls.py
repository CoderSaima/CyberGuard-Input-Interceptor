from django.urls import path
from Guard import views

urlpatterns = [
    path('', views.user_view, name='user_view')
]
