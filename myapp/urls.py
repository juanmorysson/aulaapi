from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('mapa/<str:cid>/<str:uf>/<str:br>/', views.mapa, name='mapa'),
    path('', views.endereco_list, name='endereco_list'),
    path('endereco/<int:pk>/', views.endereco_detail, name='endereco_detail'),
    path('endereco/new', views.endereco_new, name='endereco_new'),
    path('endereco/<int:pk>/edit/', views.endereco_edit, name='endereco_edit'),
    path('endereco/<pk>/remove/', views.endereco_remove, name='endereco_remove'),
    path('endereco/busca_cep', views.busca_cep, name='busca_cep'),
]