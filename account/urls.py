from django.urls import path
from .views import (RegisterUserView, login_view,
                    UpdateUserView, profile_page, logout_view)

app_name = 'account'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name='update'),
    path('profile/<email>', profile_page, name='profile'),
    path('logout/', logout_view, name='logout'),
]
