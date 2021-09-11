"""PokemonCounterEnhanced URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from Counter.views import counter_create_view, counter_update_view, counter_detail_view, counter_list_view, \
    counter_delete_view, counter_choose_view, counter_view, home_view
from Accounts.views import login_view, logout_view, signup_view

urlpatterns = [
    path('', home_view, name='home'),
    path('counter_create/', counter_create_view, name='counter_create'),
    path('counter_choose/', counter_choose_view, name='counter_choose'),
    path('<int:id>/counter/', counter_view, name='counter'),
    path('counter_list/', counter_list_view, name='counter_list'),
    path('<int:id>/counter_detail/', counter_detail_view, name='counter_detail'),
    path('<int:id>/counter_update/', counter_update_view, name='counter_update'),
    path('<int:id>/counter_delete/', counter_delete_view, name='counter_delete'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
]
