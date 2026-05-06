from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('secim/', views.hedef_sec, name='hedef_sec'),
    path('secim/ekle/<int:hedef_id>/', views.hedef_ekle, name='hedef_ekle'),
    path('secim/sil/<int:hedef_id>/', views.hedef_sil, name='hedef_sil'),
    path('hedeflerim/', views.hedeflerim, name='hedeflerim'),
    path('not-ekle/', views.not_ekle, name='not_ekle'),
    path('analizlerim/', views.analizlerim, name='analizlerim'),
]
