from django.urls import path
from .views import (
    DepartmentListView,
    EmployeeListView,
    LeadershipListView,
)

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('leadership/', LeadershipListView.as_view(), name='leadership-list'),
]