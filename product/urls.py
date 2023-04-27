from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name = 'category-list'),
    path('category/<str:id>/', views.CategoryDetailView.as_view(), name = 'category-detail'),
    path('tag/', views.TagView.as_view(), name = 'tag-list'),
    path('tag/<str:id>/', views.TagDetailView.as_view(), name = 'tag-detail'),
    path('discount/', views.DiscountView.as_view(), name = 'discount-list'),
    path('discount/<str:id>/', views.DiscountDetailView.as_view(), name = 'discount-detail'),
]
