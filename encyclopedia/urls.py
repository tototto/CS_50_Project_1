from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('random', views.randomPage, name="random"),
    path('edit', views.editPage, name="edit"),
    path('newPage', views.newPage, name="newPage"),
    path('<str:titleName>', views.title, name="title")
]
