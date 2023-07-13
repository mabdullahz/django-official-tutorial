from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # ex: /polls/5/choice/
    path("<int:question_id>/choice/", views.choice, name="choice"),
    # ex: /polls/5/vote_reset/
    path("<int:question_id>/vote_reset/", views.vote_reset, name="vote_reset"),
    # ex: /polls/new/
    path("new/", views.add_question, name="new"),
]
