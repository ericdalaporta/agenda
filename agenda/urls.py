from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('fornecedores.urls')),
    path('', include('clientes.urls')),
    path('', include('funcionarios.urls')),
    path('', include('produtos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
