from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

#自分の日報のときだけアクセスできる
class OwnerOnly(UserPassesTestMixin):
    #アクセス制限をおこなう関数
    def test_func(self):
        nippo_instance = self.get_object()
        return nippo_instance.user == self.request.user
    
    #Falseだったときのリダイレクト先を指定
    def handle_no_permission(self):
        messages.error(self.request, "ご自身の日報でのみ編集・削除可能です。")
        return redirect("nippo-detail", slug=self.kwargs["slug"])

#自分のプロフィールだけ見れるようにする
class OwnProfileOnly(UserPassesTestMixin):
    def test_func(self):
        profile_obj = self.get_object()
        try:
            return profile_obj == self.request.user.profile
        except:
            return False