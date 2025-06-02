from django.urls import path
from . import views

urlpatterns = [
    path('terms/', views.term_list, name='term-list'),
    path('terms/<int:pk>/', views.term_detail, name='term-detail'),
    path('categories/', views.category_list),
]
