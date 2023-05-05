from django.urls import path
from . import views
app_name = 'spots'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update_spot/', views.update_spot, name='update_spot'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:spot_pk>/', views.detail, name='detail'),
    path('<int:spot_pk>/comments/', views.comment_create, name='comment_create'),
    path(
        '<int:spot_pk>/comments/<int:comment_pk>/delete/',
        views.comment_delete,
        name='comment_delete',
    ),
    path('<int:spot_pk>/likes/',views.likes, name='likes'),
    path('<int:spot_pk>/comments/<int:comment_pk>/likes/',views.comment_likes, name = 'comment_likes'),
    path('search/', views.search, name='search'),
    path('delete_recently_viewed_spots/', views.delete_recently_viewed_spots, name='delete_recently_viewed_spots'),
    path('city/', views.city, name='city'),
    ]