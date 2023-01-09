from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q #インポート

class NippoModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        #qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)|
                Q(content__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("-timestamp") #新しい順に並び替えてます
    
class NippoModelManager(models.Manager):
    def get_queryset(self):
        return NippoModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class NippoModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="タイトル")
    content = models.TextField(max_length=1000, verbose_name="内容")
    public = models.BooleanField(default=False, verbose_name="公開する")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="日報"
        verbose_name_plural="日報一覧"
        
    objects = NippoModelManager()
    
    def __str__(self):
        return self.title
