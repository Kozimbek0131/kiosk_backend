from django.urls import path
from .views import EmployeeListView, DepartmentListView, LeadershipListView

urlpatterns = [
    # Bo'limlar
    path('departments/', DepartmentListView.as_view(), name='department-list'),

    # Xodimlar
    path('employees/', EmployeeListView.as_view(), name='employee-list'),

    # Rahbariyat
    path('leadership/', LeadershipListView.as_view(), name='leadership-list'),
]