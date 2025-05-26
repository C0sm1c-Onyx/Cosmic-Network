from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from profile_user.forms import ProfileForm
from profile_user.models import ProfileUser
from auth_user.models import AuthUser
from interaction_core.models import Music
from interaction_core.views import InteractionFriend


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'profile_user/edit_profile_data.html'
    model = ProfileUser

    def get_object(self):
        return get_object_or_404(ProfileUser, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.request.user.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_user_id'] = self.request.user.id
        return context


class ProfileView(View):
    def get(self, request, user_id, friend_code=None):
        profile = ProfileUser.objects.filter(user=user_id)

        context = {
            'request_user_id': request.user.id,
            'is_auth': request.user.is_authenticated,
            'user_data': AuthUser.objects.get(pk=user_id),
            'profile_data': profile[0] if profile else profile,
            'watch_user_id': request.user.id,
            'user_musics': Music.objects.filter(user=user_id),
            'friend_code': InteractionFriend.get_friend_unique_code(request.user.id, user_id)
        }

        return render(self.request, 'profile_user/profile.html', context)