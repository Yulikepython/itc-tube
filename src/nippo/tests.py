from django.test import TestCase
from nippo.models import NippoModel
from django.urls import reverse

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

class NippoTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.email = "test@itc.tokyo"
        self.password = "somepassword"
        self.title = "testTitle1"
        self.content = "testContent1"
        self.slug = "some-slug-for-test"
        super().__init__(*args, **kwargs)
        
    #初期設定
    def setUp(self):
        user_obj = User(email=self.email)
        user_obj.set_password(self.password)
        user_obj.save()
        email_obj = EmailAddress(user=user_obj, email=self.email, verified=True)
        email_obj.save()
        self.user_obj = user_obj
        nippo_obj = NippoModel(user=user_obj, title=self.title, content=self.content)
        nippo_obj.save()

    #日報の作成ができているか
    def test_saved_single_object(self):
        qs_counter = NippoModel.objects.count()
        self.assertEqual(qs_counter, 1)
    
    #ユーザーが作られているか    
    def test_user_saved(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)
        email_counter = EmailAddress.objects.count()
        self.assertEqual(email_counter, 1)
        
    #メールがverifiedになっているか    
    def test_email_verified(self):
        email_obj = EmailAddress.objects.first()
        self.assertEqual(True, email_obj.verified)
    
    #ログインページが機能しているか
    def test_login(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post("/accounts/login/", data)
        self.assertEqual(response.status_code, 200)
    
    #新規登録ページが機能しているか
    def test_signup(self):
        new_data = {"email": "test2@itc.tokyo", "password1": "somepassword2", "password2": "somepassword2"}
        redirect_to = reverse("account_email_verification_sent")
        response = self.client.post("/accounts/signup/", new_data)
        #Email Confirmationへredirectされているか？
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_to)
        #ユーザーが作られているか？
        self.assertEqual(User.objects.count(), 2)
        
    #queryが存在しない時に、404ページを返すかどうか
    def test_response_404(self):
        detail_url = reverse('nippo-detail', kwargs={"slug": "slug-not-exist"})
        detail_response = self.client.get(detail_url)
        update_url = reverse('nippo-update', kwargs={"slug": "slug-not-exist"})
        update_response = self.client.get(update_url)
        delete_url = reverse('nippo-delete', kwargs={"slug": "slug-not-exist"})
        delete_response = self.client.get(delete_url)
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
#Anonymousユーザーはアクセスできない
    def test_access_to_createview(self):
        url = reverse("nippo-create")
        redirect_to = reverse("account_login")
        response = self.client.get(url)
        self.assertRedirects(response, f"{redirect_to}?next=/nippo/create/")
        
#ログインユーザーが日報を作成する
    def test_create_on_createView(self):
        user_obj = User.objects.first()
        url = reverse('nippo-create')
        create_data = {"user": user_obj, "title": "title_from_test", "content": "content_from_test", "slug":"some-random-slug"}
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(url, create_data)
        redirect_to = reverse("nippo-list")
        qs_counter2 = NippoModel.objects.count()
        self.assertRedirects(response, redirect_to)
        self.assertEqual(qs_counter2, 2)
        
#別のユーザーではアップデートできない
    def test_update_with_another_user(self):
        another_user = User(email="test2@itc.tokyo")
        another_user.set_password("somepassword2")
        another_user.save()
        self.client.login(email=another_user.email, password=another_user.password)
        nippo_obj = NippoModel.objects.first()
        redirect_to = reverse("nippo-detail", kwargs={"slug":nippo_obj.slug})
        url = reverse('nippo-update', kwargs={"slug": nippo_obj.slug})
        response = self.client.get(url)
        self.assertRedirects(response, redirect_to)

#自分の日報はアップデートできる
    def test_update_with_own_user(self):
        self.client.login(email=self.email, password=self.password)
        nippo_obj = NippoModel.objects.first()
        url = reverse('nippo-update', kwargs={"slug": nippo_obj.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_delete_with_another_user(self):
        another_user = User(email="test2@itc.tokyo")
        another_user.set_password("somepassword2")
        another_user.save()
        self.client.login(email=another_user.email, password=another_user.password)
        nippo_obj = NippoModel.objects.first()
        redirect_to = reverse("nippo-detail", kwargs={"slug":nippo_obj.slug})
        url = reverse('nippo-delete', kwargs={"slug": nippo_obj.slug})
        response = self.client.post(url, {})
        self.assertRedirects(response, redirect_to)

    def test_delete_with_own_user(self):
        redirect_to = reverse("nippo-list")
        self.client.login(email=self.email, password=self.password)
        nippo_obj = NippoModel.objects.first()
        url = reverse('nippo-delete', kwargs={"slug": nippo_obj.slug})
        response = self.client.post(url, {})
        self.assertRedirects(response, redirect_to)

    def test_listview_with_anonymous(self):
        self.client.logout()#logoutの実行
        url = reverse("nippo-list")
        response = self.client.get(url)
        object_list = response.context_data["object_list"]
        self.assertEqual(len(object_list), 0)

    def test_listview_with_own_user(self):
        url = reverse("nippo-list")
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(url)
        object_list = response.context_data["object_list"]
        self.assertEqual(len(object_list), 1)
        
#日報を作成する（テストではない）
    def make_nippo(self, user, public):
        nippo_obj = NippoModel(user=user, public=public)
        nippo_obj.title = f"title {nippo_obj.pk}"
        nippo_obj.content = f"content {nippo_obj.pk}"
        nippo_obj.save()
        return nippo_obj
    
    #サーチフォームテスト
    def test_search_queryset(self):
        user_obj = User.objects.get(email=self.email)
        test_user = User(email="test2@itc.tokyo")
        test_user.set_password("somepassword2")
        test_user.save()
        obj1 = self.make_nippo(user=user_obj, public=True)
        obj2 = self.make_nippo(user=user_obj, public=False)
        obj3 = self.make_nippo(user=test_user, public=True)
        obj4 = self.make_nippo(user=test_user, public=False)
        counter = NippoModel.objects.count()
        self.assertEqual(counter, 5)
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse("nippo-list"))
        self.assertEqual(len(response.context_data["object_list"]), 4)
        url = reverse("nippo-list") + "?search=1"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data["object_list"]), 1)
        url = reverse("nippo-list") + "?search=content"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data["object_list"]), 4)
    
    #SlugFieldにデフォルト値が格納されているか    
    def test_slug_saved(self):
        nippo_obj = NippoModel.objects.first()
        self.assertTrue(nippo_obj.slug)