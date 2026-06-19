from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('kayit/', views.kayit, name='kayit'),

    path('ilan-ver/', views.ilan_ver, name='ilan_ver'),

    path('giris/', views.login, name='login'),

    path('cikis/', views.cikis, name='cikis'),

    path('ilan/<int:ilan_id>/', views.ilan_detay, name='ilan_detay'),

    path('basvur/<int:ilan_id>/', views.basvur, name='basvur'),

    path('basvurular/', views.basvurular, name='basvurular'),

    path('panel/', views.panel, name='panel'),

    path('basvuru-onayla/<int:basvuru_id>/', views.basvuru_onayla, name='basvuru_onayla'),

    path('basvuru-reddet/<int:basvuru_id>/', views.basvuru_reddet, name='basvuru_reddet'),

    path('basvurularim/', views.basvurularim, name='basvurularim'),

    path('profil/', views.profil, name='profil'),

    path('ilan-sil/<int:ilan_id>/', views.ilan_sil, name='ilan_sil'),

    path('ilan-duzenle/<int:ilan_id>/', views.ilan_duzenle, name='ilan_duzenle'),

    path('calisan/<int:kullanici_id>/', views.calisan_detay, name='calisan_detay'),

    path('basvuru-sil/<int:basvuru_id>/', views.basvuru_sil, name='basvuru_sil'),

    path('puanla/', views.puanla_sayfasi, name='puanla_sayfasi'),
    
    path('puan-ver/<int:basvuru_id>/', views.puan_ver, name='puan_ver'),
]
