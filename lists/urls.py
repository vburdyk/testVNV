from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),

    path('group-list/', views.group_list, name='group_list'),
    path('delete-group/<int:pk>/', views.delete_group, name='group_delete'),

    path('sign-in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout, name='logout'),

    path('create/', views.create_user, name='user_create'),
    path('delete/<int:pk>/', views.delete_user, name='user_delete'),
    path('edit/<int:pk>/', views.user_edit, name='user_edit'),
]
