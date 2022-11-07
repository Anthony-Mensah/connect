from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    #UPLOAD POST
    path('upload-post/', views.upload_post, name='upload_post'),
    #VIEW POST
    path('view-post/<str:pk>/', views.view_post, name='view_post'),
    #DELETE POST
    path('delete_post/<str:pk>/', views.delete_post, name='delete_post'),
    #FAVORTIE POST
    path('add-favorite/<str:pk>/', views.add_favorite, name='add_favorite'),
    #REMOVE FAVORITE
    path('remove-favorite/<str:pk>/', views.remove_favorite, name='remove_favorite'),
    #FAVORITE POST
    path('favorites/', views.favorites, name='favorites'),
    #PROFILE PAGE
    path('profile/<str:pk>/', views.profile, name='profile'),
    #FOLLOW
    path('follow/<str:pk>/', views.follow, name='follow'),
    # SEARCH RUL
    path('search-results/', views.search_result, name='search_result')
]
