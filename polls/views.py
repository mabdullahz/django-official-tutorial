from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.utils import timezone

from django.shortcuts import get_object_or_404, render, redirect

from .models import Question, Choice

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_to_lobby(msg):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'chat_lobby',
        {
            "type": "chat.message",
            'message': msg,
        }
    )

def index(request):
    if request.user.is_authenticated:
        return redirect("/polls/home")
    return render(request, "polls/index.html", {})


class HomeView(LoginRequiredMixin, generic.ListView):
    login_url = "/polls"
    template_name = "polls/home.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/polls"
    model = Question
    template_name = "polls/detail.html"


class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = "/polls"
    model = Question
    template_name = "polls/results.html"

@login_required(login_url="/polls")
def choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'GET':
        return render(request, "polls/choice.html", {"question": question})
    elif request.method == 'POST':
        user_submitted_choice = request.POST["choice"]
        if not user_submitted_choice:
            return render(request, "polls/choice.html", {
                "question": question,
                "error_message": "Please enter a valid choice"
            })

        new_choice = Choice(
            question=question,
            choice_text=user_submitted_choice,
        )
        new_choice.save()
        send_to_lobby(f'<i>{request.user.username}</i> added a new choice to the question <a href="{reverse("polls:detail", args=(question.id,))}">"{question.question_text}"</a>')
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

@login_required(login_url="/polls")
def vote_reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    for choice in question.choice_set.all():
        choice.votes = 0
        choice.save()

    send_to_lobby(f'<i>{request.user.username}</i> reset the votes for question <a href="{reverse("polls:detail", args=(question.id,))}">"{question.question_text}"</a>')
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@login_required(login_url="/polls")
def add_question(request):
    if request.method == 'GET':
        return render(request, "polls/new_question.html", {})
    elif request.method == 'POST':
        user_submitted_question = request.POST["question"]
        if not user_submitted_question:
            return render(request, "polls/new_question.html", {
                "error_message": "Please enter a valid question"
            })
        
        new_question = Question(
            question_text=user_submitted_question,
            pub_date=timezone.now(),
        )
        new_question.save()
        send_to_lobby(f'<i>{request.user.username}</i> just added a new question <a href="{reverse("polls:detail", args=(new_question.id,))}">"{new_question.question_text}"</a>')
    return HttpResponseRedirect(reverse("polls:home",))

@login_required(login_url="/polls")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        send_to_lobby(f'<i>{request.user.username}</i> just vote on <a href="{reverse("polls:detail", args=(question.id,))}">"{question.question_text}"</a>')
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def login_user(request):
    data = request.POST
    user = authenticate(request, username=data['username'], password=data['password'])

    if user is not None:
        login(request, user)
        send_to_lobby(f'<i>{request.user.username}</i> just logged in!')
        return HttpResponseRedirect(reverse("polls:home"))
    else:
        return render(request, "polls/index.html", {
            "login_message": "Wrong username/password",
        })


@login_required(login_url="/polls")
def logout_user(request):
    username = request.user.username
    logout(request)
    send_to_lobby(f'<i>{username}</i> just logged out!')
    return HttpResponseRedirect(reverse("polls:index"))

def register(request):
    data = request.POST
    u = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['fname'],
        last_name=data['lname'],
    )

    u.save()
    send_to_lobby(f'<i>{data["username"]}</i> just registered for a new account!')

    return render(request, "polls/index.html", {
        "register_message": "Successfully registered, please login using your email/password now",
    })
