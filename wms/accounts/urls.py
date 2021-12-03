from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('users/', views.users_view, name="users"),
    path('sales/', views.sales_view, name="sales"),
    path('stores/', views.store, name="stores"),
    path('regions/', views.region, name="regions"),

    path('update_user/<str:pk>/', views.updateUser, name="update_user"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('create_product', views.createProduct, name="create_product"),
    path('update_product/<str:pk>/', views.updateProduct, name="update_product"),
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),

    path('create_sale', views.createSales, name="create_sale"),
    path('update_sale/<str:pk>/', views.updateSales, name="update_sale"),
    path('delete_sale/<str:pk>/', views.deleteSale, name="delete_sale"),

    path('create_store', views.createStore, name="create_store"),
    path('update_store/<str:pk>/', views.updateStore, name="update_store"),
    path('delete_store/<str:pk>/', views.deleteStore, name="delete_store"),
    
]