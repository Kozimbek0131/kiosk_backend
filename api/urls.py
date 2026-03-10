from django.urls import path
from .views import (
    EmployeeListView,
    DepartmentListView,
    LeadershipListView,
    upload_employee_photo,
    upload_leadership_photo,
)

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:employee_id>/upload-photo/', upload_employee_photo, name='employee-upload-photo'),
    path('leadership/', LeadershipListView.as_view(), name='leadership-list'),
    path('leadership/<int:leader_id>/upload-photo/', upload_leadership_photo, name='leadership-upload-photo'),
]