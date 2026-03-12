from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee, Department, Leadership
from .serializers import EmployeeSerializer, DepartmentSerializer, LeadershipSerializer
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY) if settings.SUPABASE_KEY else None
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name_uz', 'full_name_ru', 'full_name_en', 'position_uz', 'phone']
    filterset_fields = ['floor', 'department']
    ordering_fields = ['floor', 'room', 'full_name_uz']
    ordering = ['floor', 'room']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LeadershipListView(generics.ListAPIView):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


def _upload_to_supabase(file, folder, record_id):
    ext = file.name.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Faqat {', '.join(ALLOWED_EXTENSIONS)} formatlar ruxsat etilgan")
    file_path = f"{folder}/{record_id}.{ext}"
    file_bytes = file.read()
    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=file_path, file=file_bytes,
        file_options={"content-type": file.content_type, "upsert": "true"}
    )
    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_path)


@csrf_exempt
@require_http_methods(["POST"])
def upload_employee_photo(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Hodim topilmadi"}, status=404)
    photo = request.FILES.get("photo")
    if not photo:
        return JsonResponse({"error": "Rasm yuborilmadi"}, status=400)
    try:
        photo_url = _upload_to_supabase(photo, "employees", employee_id)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    employee.image = photo_url
    employee.save(update_fields=["image"])
    return JsonResponse({"success": True, "employee_id": employee_id, "photo_url": photo_url})


@csrf_exempt
@require_http_methods(["POST"])
def upload_leadership_photo(request, leader_id):
    try:
        leader = Leadership.objects.get(id=leader_id)
    except Leadership.DoesNotExist:
        return JsonResponse({"error": "Rahbar topilmadi"}, status=404)
    photo = request.FILES.get("photo")
    if not photo:
        return JsonResponse({"error": "Rasm yuborilmadi"}, status=400)
    try:
        photo_url = _upload_to_supabase(photo, "leadership", leader_id)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    leader.image = photo_url
    leader.save(update_fields=["image"])
    return JsonResponse({"success": True, "leader_id": leader_id, "photo_url": photo_url})