from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),


    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('user', views.userPage, name='user'),
    path('products/', views.products, name='products'),
    path('profile/', views.profileSettings, name='profile'),
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),

    path('create_order/', views.createOrder, name='create_order'),
    path('place_new_order/<str:pk>/', views.placeNewOrder, name='place_new_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('order_summary/<str:pk>/', views.orderSummary, name='order_summary'),

    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),
    path('create_customer/', views.createCustomer, name='create_customer'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),#default for me to reset my password (submit email form here)
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),#default (email sent success message)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),#default (link to password reset form in email
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),#default (password changed success message)
    #all required password reset views have been created by default django
]
