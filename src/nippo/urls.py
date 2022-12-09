from django.urls import path
from .views import nippoListView
 
urlpatterns = [
  path("", nippoListView),
]