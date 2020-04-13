"""Projet_08 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'Nutella'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('legals/', views.LegalView.as_view(), name='legals'),
    path('results/', views.ResultsView.as_view(), name='results'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('saved_food/', views.SavedFoodView.as_view(), name='saved_food'),
    path('product/<int:pk>', views.ProductView.as_view(), name='product'),
    path('delete/<int:product_id>', views.DeleteView.as_view(), name='delete'),
    path('add_to_favorite/<int:product_id>',
         views.AddToFavoriteView.as_view(), name='add_to_favorite'),
]
