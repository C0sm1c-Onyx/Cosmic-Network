from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('id<int:user_id>/', profile, name='profile'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_cn, name='logout_cn'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('add_post/', add_post, name='add_post'),
    path('id<int:user_id>/subscribe/', subscribe),
    path('id<int:user_id>/delete_post/<int:post_id>/', delete_post),
    path('id<int:user_id>/like_post/<int:post_id>/', like_post),
    path('like_news/<int:post_id>/', like_news),
    path('search_users/', search_users, name='search_users'),
    path('id<int:user_id>/comments/<int:post_id>/', comments),
    path('id<int:user_id>/delete_comment/<int:post_id>/<int:comment_id>/', delete_comment),
    path('id<int:user_id>/message/', message),
]