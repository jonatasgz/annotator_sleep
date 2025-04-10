from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('api/', include('nlp.urls')),
    path('admin/', admin.site.urls),
    path('health/', health_check),
]
