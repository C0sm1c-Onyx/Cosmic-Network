from django.urls import path

from profile_user.views import EditProfileView, ProfileView
from interaction_core.views import InteractionFriend
from messenger.views import pre_initial_chat


urlpatterns = [
    path('profile/id<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/id<int:user_id>/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/id<int:user_id>/add-friend/', InteractionFriend.add_friend),
    path('profile/id<int:user_id>/delete-friend/<int:friend_code>/', InteractionFriend.delete_friend),
    path('profile/id<int:user_id>/pre-init-chat/', pre_initial_chat, name='pre-init-chat'),
]