from django.urls import path

from interaction_core.views import (
    add_music, FriendListView, FriendRequestsListView,
    InteractionFriend, search,
)


urlpatterns = [
    path('profile/id<int:user_id>/add_music/', add_music, name='add_music'),

    path('friends/', FriendListView.as_view(), name='friends'),
    path('friends/requests/', FriendRequestsListView.as_view(), name='requests'),
    path('friends/requests/accept/<int:friend_code>/', InteractionFriend.accept_friend),
    path('friends/requests/reject/<int:friend_code>/', InteractionFriend.delete_friend),

    path('search/', search, name='search'),
]