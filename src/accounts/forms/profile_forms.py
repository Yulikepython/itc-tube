from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_email = self.instance.user.email
        if username == user_email:
            raise forms.ValidationError("ユーザー名を変更してください")
        elif "@" in username:
            raise forms.ValidationError("ユーザー名にEメールアドレスは使用できません")
        return username