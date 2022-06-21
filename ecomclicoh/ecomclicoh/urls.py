from django.contrib import admin
from django.urls import path, include
from users.api.views import UserLogin
from products.api.viewsets import OrderViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users-login/', UserLogin.as_view(), name='users-login'),
    path('users/',include('users.api.routers')),
    path('product-api/',include('products.api.routers')),

]
