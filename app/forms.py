from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sex'].empty_label = 'Not indicated'

    class Meta:
        model = Profile
        fields = ('photo', 'status', 'phone', 'birthdate', 'sex')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('text', 'image', 'video', 'music')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messanger
        fields = ('text', 'image', 'video', 'music')