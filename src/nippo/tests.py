from django.test import TestCase
from nippo.models import NippoModel
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

class NippoTestCase(TestCase):
    #初期設定
    def setUp(self):
        self.email = "test@itc.tokyo"
        self.password = "somepass"
        user_obj = User(email=self.email)
        user_obj.set_password(self.password)
        user_obj.save()
        self.user_obj = user_obj
        # self.email_obj = self.user_obj.emailaddress_set.first()
        # self.email_obj.verified = True
        # self.email_obj.save()
        obj = NippoModel(title="testTitle1", content="testContent1", user=self.user_obj)
        obj.save()

    #日報の作成ができているか
    def test_saved_single_object(self):
        qs_counter = NippoModel.objects.count()
        self.assertEqual(qs_counter, 1)
    
    #queryが存在しない時に、404ページを返すかどうか
    def test_response_404(self):
        detail_url = reverse('nippo-detail', kwargs={"pk": 100})
        detail_response = self.client.get(detail_url)
        update_url = reverse('nippo-update', kwargs={"pk": 100})
        update_response = self.client.get(update_url)
        delete_url = reverse('nippo-delete', kwargs={"pk": 100})
        delete_response = self.client.get(delete_url)
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)

    # #createページできちんとデータが保存されているか
    def test_create_on_createView(self):
        self.client.force_login(self.user_obj) #アクセス制限により、ログインしなければCreateViewでの処理をおこなえない
        url = reverse('nippo-create')
        create_data = {"title": "title_from_test", "content": "content_from_test"}
        response = self.client.post(url, create_data)
        qs_counter2 = NippoModel.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs_counter2, 2)
        
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