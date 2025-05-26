from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from interaction_core.forms import AddMusicForm
from interaction_core.models import Music, Friends
from auth_user.models import AuthUser
from profile_user.models import ProfileUser


class InteractionFriend:
    def get_all_friends(self, request):
        return self.base_interaction(request, status=True, method='get-friends')

    def get_all_requests(self, request):
        return self.base_interaction(request, status=False, method='get-requests')

    @staticmethod
    def base_interaction(request, status=False, method=None):
        if method == 'get-requests':
            queryset = Friends.objects.filter(
                friend=request.user.id, status=status
            )

            return queryset

        elif method == 'get-friends':
            queryset = Friends.objects.filter(
                Q(friend=request.user.id, status=status)
                |
                Q(user=request.user.id, status=status)
            )

            filter_friends = []
            for obj in queryset:
                if (obj.user.id != request.user.id) and not (obj.user in filter_friends):
                    filter_friends.append(obj.user)

                if (obj.friend.id != request.user.id) and not (obj.friend in filter_friends):
                    filter_friends.append(obj.friend)

            return filter_friends

    @staticmethod
    def get_friend_unique_code(user_id, friend_id):
        instance = Friends.objects.filter(
            Q(user=user_id, friend=friend_id)
            |
            Q(user=friend_id, friend=user_id)
        )

        return instance[0].friend_unique_code if instance else instance

    @staticmethod
    def add_friend(request, user_id):
        Friends.objects.create(
            user=AuthUser.objects.get(pk=request.user.id),
            friend=AuthUser.objects.get(pk=user_id)
        )

        return redirect(f'/profile/id{user_id}/')

    @staticmethod
    def accept_friend(request, friend_code):
        instance = Friends.objects.get(friend_unique_code=friend_code)
        instance.status = True
        instance.save()

        return redirect('requests')

    @staticmethod
    def delete_friend(request, friend_code, user_id=None):
        Friends.objects.get(friend_unique_code=friend_code).delete()

        if 'profile' in request.path:
            return redirect(f'/profile/id{user_id}/')

        return redirect('requests')


class FriendListView(View, InteractionFriend):
    def get(self, request):
        context = {
            'is_auth': request.user.is_authenticated,
            'request_user_id': request.user.id,
            'user_friend_list': [
                (friend, ProfileUser.objects.get(user=friend)) for friend in self.get_all_friends(request)
            ]
        }

        return render(
            request, 'interaction_core/friends.html', context
        )


class FriendRequestsListView(View, InteractionFriend):
    def get(self, request):
        context = {
            'is_auth': request.user.is_authenticated,
            'request_user_id': request.user.id,
            'user_friend_request': [
                (friend, ProfileUser.objects.get(user=friend.user_id)) for friend in self.get_all_requests(request)
            ]
        }

        return render(
            request, 'interaction_core/friend_requests.html', context
        )


def add_music(request, user_id):
    if request.method == 'POST':
        form = AddMusicForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['user'] = AuthUser.objects.get(pk=user_id)
            Music.objects.create(**form.cleaned_data)
            return redirect(f'/profile/id{user_id}/')
    else:
        form = AddMusicForm()

    context = {
        'form': form,
        'request_user_id': request.user.id,
        'is_auth': request.user.is_authenticated,
    }

    return render(request, 'interaction_core/add_music.html', context)


def search(request):
    search_query = request.GET.get('search')
    if search_query:
        if len(search_query.split()) == 2:
            first_name, last_name = search_query.split()

            queryset = AuthUser.objects.filter(
                Q(first_name__icontains=first_name)
                &
                Q(last_name__icontains=last_name)
                |
                Q(first_name__icontains=last_name)
                &
                Q(last_name__icontains=first_name)
            )

            queryset = [(user, ProfileUser.objects.get(user=user)) for user in queryset]
        else:
            queryset = AuthUser.objects.filter(
                Q(first_name__icontains=search_query)
                |
                Q(last_name__icontains=search_query)
                |
                Q(connection_code__icontains=search_query)
            )

            queryset = [(user, ProfileUser.objects.get(user=user)) for user in queryset]
    else:
        queryset = [(user, ProfileUser.objects.get(user=user)) for user in AuthUser.objects.all()]

    context = {
        'user_list': queryset,
        'request_user_id': request.user.id,
        'is_auth': request.user.is_authenticated
    }

    return render(request, 'interaction_core/search.html', context)