from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('', views.homepage, name="home"),
    path('logout/', views.logout_user, name="logout"),
    path('download-pool/<int:pk>/', views.download_pool, name="download_pool"),
]
