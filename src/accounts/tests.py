from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from django.contrib.auth import get_user_model, login
from accounts.models import Profile

User = get_user_model()
signup_url = reverse("account_signup")
login_url = reverse("account_login")

class UserTestCase(TestCase):
    # signupページでユーザーを作成し、Eメール確認も済にする
    def setUp(self):
        self.email = "test@itc.tokyo"
        self.password = "somepass"
        self.res = self.client.post(signup_url, {"email": self.email, "password1": self.password, "password2": self.password})
        self.user_obj = User.objects.first()
        self.email_obj = self.user_obj.emailaddress_set.first()
        self.email_obj.verified = True
        self.email_obj.save()

    # singupページからのレスポンスが正しいか？
    def test_signup(self):
        self.assertEqual(self.res.status_code, 302)
        self.assertEqual(self.res.url, "/accounts/confirm-email/")

    # ユーザーがきちんと作らているか？
    def test_single_user(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)
        self.assertEqual(self.user_obj.email, self.email)

    #メールアドレスがverifiedになっているか？
    def test_emailaddress_verified(self):
        self.assertEqual(self.email_obj.verified, True)

    # ログインページでのpostが正しく動作するか
    def test_login_page(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, 200)

    # ログアウトの際にログインページへリダイレクトされているか？
    def test_logout(self):
        res = self.client.get("/accounts/logout/")
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, login_url)

    # verifiedされているユーザーの場合はきちんとログインできているか？
    def test_verified_user_login(self):
        c = Client()
        res_bool = c.login(email=self.email, password=self.password)
        self.assertEqual(res_bool, True)
    
    # verifiedされていないユーザーの場合はログインできない？
    def test_not_verified_user_login(self):
        res = self.client.post(signup_url, {"email": "not-verifed@itc.tokyo", "password1": "somepassword", "password2": "somepassword"})
        self.assertEqual(res.status_code, 302)
        c = Client()
        res_bool = c.login(email="not-verified@itc.tokyo", password="somepassword")
        self.assertEqual(res_bool, False)

class AccountsTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.email = "test@itc.tokyo"
        self.password = "somepassword"
        super().__init__(*args, **kwargs)

    def setUp(self):
        user_obj = User(email=self.email)
        user_obj.set_password(self.password)
        user_obj.save()

    def test_profile_saved(self):
        counter = Profile.objects.count()
        self.assertEqual(counter, 1)
        profile_obj = Profile.objects.first()
        self.assertEqual(profile_obj.user.email, profile_obj.username)