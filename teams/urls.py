from django.urls import path

from . import views

urlpatterns = [
    path('', views.TeamControl.as_view()),
    path('<int:id>', views.TeamDetail.as_view()),
]
