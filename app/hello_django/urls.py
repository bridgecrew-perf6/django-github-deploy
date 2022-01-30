from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def home(request):
    return JsonResponse({"hello": "world!"})


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
