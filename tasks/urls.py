from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeaponListView.as_view(), name='task-list'),
    path('<int:pk>/', views.WeaponDetailView.as_view(), name='task-detail'),
    path('transactions/', views.TransactionListView.as_view(), name='member-list'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('suppliers/', views.SupplierListView.as_view(), name='supplier-list'),
]
