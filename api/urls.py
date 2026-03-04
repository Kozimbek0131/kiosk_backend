from django.urls import path
from .views import EmployeeListView  # Agar view nomingiz boshqacha bo'lsa, o'shani yozing

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
]