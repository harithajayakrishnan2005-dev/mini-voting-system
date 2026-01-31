from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_module import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_module.urls')),
    path('admin-module/', include(('admin_module.urls', 'admin_module'), namespace='admin_module')),
    path('', user_views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
