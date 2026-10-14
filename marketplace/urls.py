from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('item/create/', views.ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('item/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('search/', views.ItemSearchView.as_view(), name='item-search'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('search/', views.ItemSearchView.as_view(), name='item-search'),
    path('my-listings/', views.MyListingsView.as_view(), name='my-listings'),
    path('item/<int:pk>/review/', views.ReviewCreateView.as_view(), name='review-create'),
]