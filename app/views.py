from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *
from .models import *


def profile(request, user_id):
    posts = Content.objects.filter(author=user_id)
    data = Profile.objects.filter(user_id=user_id)
    templates = {'name': User.objects.get(id=user_id).username,
                 'data': data[0] if data else data,
                 'id1': user_id,
                 'id2': request.user.id,
                 'posts': posts,
                 'is_subs': Followers.objects.filter(user=user_id, follower=request.user.id),
                 'count_followers': sum(1 for _ in Followers.objects.filter(user=user_id)),
                 'count_likes': Likes.objects.filter(content__author=user_id).count(),
                 'profile': Profile.is_online(request, user_id),
                 'reg_date': User.objects.get(id=user_id).date_joined,
                 'count_video': Video.objects.filter(user=user_id).count(),
                 'count_audio': Music.objects.filter(user=user_id).count(),
                 'count_photo': Photo.objects.filter(user=user_id).count(),
    }

    return render(request, 'app/profile.html', context=templates)


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Регистрация прошла успешно. Войдите'


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'app/login.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.request.user.id,))


def index(request):
    templates = {
        'is_auth': request.user.is_authenticated,
        'user_id': request.user.id,
        'content_subs': Content.objects.filter(author__user__in=Followers.objects.filter(follower=request.user.id))
    }

    return render(request, 'app/base.html', templates)


def logout_cn(request):
    logout(request)
    return redirect('home')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile_data = Profile.objects.get(user_id=request.user.id)
                if profile_data.photo and not form.cleaned_data['photo']:
                    del form.cleaned_data['photo']
                if profile_data.sex and not form.cleaned_data['sex']:
                    del form.cleaned_data['sex']
                if profile_data.status and not form.cleaned_data['status']:
                    del form.cleaned_data['status']
                if profile_data.phone and not form.cleaned_data['phone']:
                    del form.cleaned_data['phone']
                if profile_data.birthdate and not form.cleaned_data['birthdate']:
                    del form.cleaned_data['birthdate']

                Profile.objects.filter(user_id=request.user.id).update(**form.cleaned_data)
                return redirect(f'/id{request.user.id}/')

            except:
                form.cleaned_data['user'] = User.objects.get(id=request.user.id)
                Profile.objects.create(**form.cleaned_data)
                return redirect(f'/id{request.user.id}/')
    else:
        form = EditProfileForm()

    return render(request, 'app/edit_profile.html', {'form': form, 'user_id': request.user.id})


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data['author'] = User.objects.get(id=request.user.id)
            Content.objects.create(**form.cleaned_data)
            return redirect(f'/id{request.user.id}/')

    else:
        form = AddPostForm()

    templates = {'form': form}
    return render(request, 'app/add_post.html', templates)


def subscribe(request, user_id):
    id1, id2 = User.objects.get(id=request.user.id), User.objects.get(id=user_id)
    try:
        Followers.objects.get(user=id2, follower=id1).delete()
        return redirect(f'/id{id2.id}/')
    except:
        Followers.objects.create(user=id2, follower=id1)
        return redirect(f'/id{id2.id}/')


def delete_post(request, user_id, post_id):
    Content.objects.filter(id=post_id).delete()
    return redirect(f'/id{request.user.id}')


def like_post(request, user_id, post_id):
    post = Content.objects.get(id=post_id)
    try:
        Likes.objects.get(user=request.user.id, content=post_id).delete()
        return redirect(f'/id{user_id}')
    except:
        Likes.objects.create(user=request.user, content=post)
        return redirect(f'/id{user_id}')


def like_news(request, post_id):
    post = Content.objects.get(id=post_id)
    try:
        Likes.objects.get(user=request.user.id, content=post_id).delete()
        return redirect('home')
    except:
        Likes.objects.create(user=request.user, content=post)
        return redirect('home')


def search_users(request):
    templates = {
        'all_users': User.objects.all().order_by('username')
    }

    return render(request, 'app/search_users.html', templates)


def comments(request, user_id, post_id):
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.cleaned_data['user'] = User.objects.get(id=request.user.id)
            form.cleaned_data['content'] = Content.objects.get(id=post_id)
            Comment.objects.create(**form.cleaned_data)
            return redirect(f'/id{user_id}/comments/{post_id}')

    else:
        form = CommentsForm()

    templates = {'form': form,
                 'post': Content.objects.get(id=post_id),
                 'comments': Comment.objects.filter(content=post_id),
                 'id1': request.user.id,
                 'id2': user_id,
                }

    return render(request, 'app/comments.html', templates)


def delete_comment(request, user_id, comment_id, post_id):
    Comment.objects.get(user=request.user.id, id=comment_id).delete()
    return redirect(f'/id{user_id}/comments/{post_id}')


def message(request, user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.cleaned_data['user1'] = User.objects.get(id=request.user.id)
            form.cleaned_data['user2'] = User.objects.get(id=user_id)
            Messanger.objects.create(**form.cleaned_data)
            return redirect(f'/id{user_id}/message/')

    else:
        form = MessageForm()

    all_message = Messanger.objects.filter(user1=request.user.id, user2=user_id) | Messanger.objects.filter(user1=user_id, user2=request.user.id)
    templates = {
                 'form': form,
                 'name': User.objects.get(id=user_id).username,
                 'all_message': all_message.order_by('datetime'),
                 'photo1': Profile.objects.get(user=request.user.id).photo,
                 'photo2': Profile.objects.get(user=user_id).photo,
                 'id1': request.user.id,
                 'id2': user_id,
                }

    return render(request, 'app/message.html', templates)