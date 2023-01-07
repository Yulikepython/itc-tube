from django import forms
from django.forms.fields import DateField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm

from .models import User, Profile, GENDER_CHOICE

#GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]はmodels.pyで定義してます

class CustomAdminChangeForm(UserChangeForm):
#Profileクラスのフィールドを追記します
    username = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100, required=False)
    phone_number = forms.IntegerField(required=False) 
    gender = forms.ChoiceField(choices=GENDER_CHOICE, required=False)
    birthday = DateField(required=False)

    class Meta:
        model = User
        fields =('email', 'password', 'active', 'admin')

#Profileが存在する場合は、初期値にデータを格納する
    def __init__(self, *args, **kwargs):
        user_obj = kwargs["instance"]
        if hasattr(user_obj, "profile"):
            profile_obj = user_obj.profile
            self.base_fields["username"].initial = profile_obj.username
            self.base_fields["department"].initial = profile_obj.department
            self.base_fields["phone_number"].initial = profile_obj.phone_number
            self.base_fields["gender"].initial = profile_obj.gender
            self.base_fields["birthday"].initial = profile_obj.birthday
        super().__init__(*args, **kwargs)

#保存機能の定義
    def save(self, commit=True):
        user_obj = super().save(commit=False)
        username = self.cleaned_data.get("username")
        department = self.cleaned_data.get("department")
        phone_number = self.cleaned_data.get("phone_number")
        gender = self.cleaned_data.get("gender")
        birthday = self.cleaned_data.get("birthday")
        if hasattr(user_obj, "profile"):
            profile_obj = user_obj.profile
        else:
            profile_obj = Profile(user=user_obj)
        if username is not None:
            profile_obj.username = username
        if department is not None:
            profile_obj.department = department
        if phone_number is not None:
            profile_obj.phone_number = phone_number
        if gender is not None:
            profile_obj.gender=gender
        if birthday is not None:
            profile_obj.birthday = birthday
        profile_obj.save()
        if commit:
            user_obj.save()
        return user_obj

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