from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('students/', views.student_list, name="student_list"),
]
