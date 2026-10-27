from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app_home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('prochistka-kanalizatsii/', views.prochistka, name='prochistka'),
    path('santekhnicheskie-raboty/', views.santehnika, name='santehnika'),
    path('o-nas/', views.about, name='about'),
    path('kontakty/', views.contacts, name='contacts'),
    path('feedback/', views.feedback, name='feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
