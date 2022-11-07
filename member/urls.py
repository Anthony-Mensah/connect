#MEMBER MEMBER MEMBER
from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.signup, name='signup'),
    #LOGIN
    path('login/', views.login, name='login'),
    #LOGOUT
    path('logout/', views.logout, name='logout'),
    #SETTINGS
    path('settings/', views.settings, name='settings'),
    # CHANGE PASSSORD
    # path('settings/change-password/', views.change_password, name='change_password')
]
