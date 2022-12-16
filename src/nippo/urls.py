from django.urls import path
from .views import nippoListView, nippoDetailView,nippoCreateView, nippoUpdateFormView, nippoDeleteView
 
urlpatterns = [
  path("", nippoListView, name="nippo-list"),
  path("detail/<int:pk>/", nippoDetailView, name="nippo-detail"),
  path("create/", nippoCreateView, name="nippo-create"),
  path("update/<int:pk>/", nippoUpdateFormView, name="nippo-update"),
  path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),
]