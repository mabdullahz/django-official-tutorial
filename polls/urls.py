from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path("register/", views.HomeView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # ex: /polls/5/choice/
    path("<int:question_id>/choice/", views.choice, name="choice"),
    # ex: /polls/5/vote_reset/
    path("<int:question_id>/vote_reset/", views.vote_reset, name="vote_reset"),
    # ex: /polls/new/
    path("new/", views.add_question, name="new"),
]
