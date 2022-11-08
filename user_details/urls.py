from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.UserControl.as_view()),
    path('user/<str:username>', views.UserDetail.as_view()),
    path('coach/', views.CoachControl.as_view()),
    path('coach/<int:id>', views.CoachDetail.as_view()),
    path('player/', views.PlayerControl.as_view()),
    path('player/<int:id>', views.PlayerDetail.as_view()),
]