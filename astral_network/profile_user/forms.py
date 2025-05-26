from django import forms

from profile_user.models import ProfileUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = (
            'photo', 'birthdate', 'about_yourself',
            'status', 'gender'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'not specified'