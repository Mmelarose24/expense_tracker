from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Expenses
    path('expenses/', views.expenses_list, name='expenses_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    
    # Budgets
    path('budgets/', views.budgets_list, name='budgets_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    
    # Schedules
    path('schedules/', views.schedules_list, name='schedules_list'),
    path('schedules/add/', views.add_schedule, name='add_schedule'),
    
    # Categories
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.add_category, name='add_category'),
    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('logout/', views.user_logout, name='logout'),
]