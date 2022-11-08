from django.urls import path

from . import views

urlpatterns = [
    path('', views.MatchControl.as_view()),
    path('<int:id>', views.MatchDetail.as_view()),
]
