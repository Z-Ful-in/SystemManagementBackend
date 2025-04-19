from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/register', views.register_view, name='register'),

    path('images/user/<str:username>', views.get_user_images, name='get_user_images'),
    path('images/<int:id>', views.delete_image, name='delete_image'),
]