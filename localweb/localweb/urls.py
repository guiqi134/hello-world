"""localweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('get_password/', views.get_password, name='get_password'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('rider/', views.rider, name='rider'),
    path('index/restaurant/<str:pk>/', views.restaurant_detail, name='restaurant-detail'),
    path('index/cart/', views.get_cart),
    path('index/restaurant/guiqi1234/additem/<uuid:food_id>/', views.add_to_cart, name='additem'),
    path('index/cart/removeitem/<uuid:food_id>/', views.remove_from_cart, name='removeitem'),
    path('index/customer_order/', views.customer_order, name='customer_order'),
    path('restaurant/restaurant_order/', views.restaurant_order, name='restaurant_order'),
    path('rider/rider_order/', views.rider_order, name='rider_order'),
]

# Use include() to add paths from the catalog application 
from django.conf.urls import include

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/')),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)