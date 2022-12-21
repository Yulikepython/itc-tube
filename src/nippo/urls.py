from django.urls import path
from .views import NippoListView, NippoDetailView, nippoListView, nippoDetailView,nippoCreateView, nippoUpdateFormView, nippoDeleteView
 
urlpatterns = [
  path("", NippoListView.as_view(), name="nippo-list"),
  path("detail/<int:pk>/", NippoDetailView.as_view(), name="nippo-detail"),
  # path("", nippoListView, name="nippo-list1"),
  # path("detail/<int:pk>/", nippoDetailView, name="nippo-detail"),
  path("create/", nippoCreateView, name="nippo-create"),
  path("update/<int:pk>/", nippoUpdateFormView, name="nippo-update"),
  path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),
]