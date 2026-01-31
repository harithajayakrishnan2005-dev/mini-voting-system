
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Option, Vote
from django.contrib import messages
from .models import UserProfile, Vote, Poll, Option

from .models import Poll, Option, Vote
from .models import Feedback, Poll

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registered successfully! You can now login.")
            return redirect('user:login')

    return render(request, 'user_module/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('user:dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'user_module/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('user:login')


@login_required
def submit_feedback(request):
    polls = Poll.objects.all()  

    if request.method == "POST":
        poll_id = request.POST.get("poll_id")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating and not comment:
            messages.error(request, "Please provide a rating or comment.")
            return redirect('user:feedback')

        feedback = Feedback(user=request.user)

      
        if poll_id:
            try:
                feedback.poll = Poll.objects.get(id=poll_id)
            except Poll.DoesNotExist:
                feedback.poll = None

        
        if rating:
            feedback.rating = int(rating)
        if comment:
            feedback.comment = comment.strip()  

        feedback.save()
        messages.success(request, "Feedback submitted successfully!")
        return redirect('user:feedback')

    return render(request, 'user_module/feedback.html', {"polls": polls})


@login_required
def user_dashboard(request):
    return render(request, 'user_module/dashboard.html')


@login_required
def user_profile(request):
    user_profile = request.user.userprofile
    return render(request, 'user_module/profile.html', {'user_profile': user_profile})

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'user_module/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def my_votes(request):
    votes = Vote.objects.filter(user=request.user).select_related('poll', 'option')
    return render(request, 'user_module/my_vote.html', {'votes': votes})


def index(request):
    return render(request, 'user_module/index.html')


@login_required
def poll_list(request):
    polls = Poll.objects.prefetch_related('options')
    voted_polls = Vote.objects.filter(
        user=request.user
    ).values_list('poll_id', flat=True)

    return render(request, 'user_module/poll_list.html', {
        'polls': polls,
        'voted_polls': voted_polls
    })


@login_required
def submit_vote(request, poll_id):
    if request.method != "POST":
        return redirect('user:poll_list')

    poll = get_object_or_404(Poll, id=poll_id)

    if Vote.objects.filter(poll=poll, user=request.user).exists():
        messages.warning(request, "You already voted for this poll ")
        return redirect('user:poll_list')

    option_id = request.POST.get('option')
    if not option_id:
        messages.error(request, "Please select an option ")
        return redirect('user:poll_list')

    option = get_object_or_404(Option, id=option_id)

    Vote.objects.create(
        poll=poll,
        option=option,
        user=request.user
    )

    messages.success(request, "Vote submitted successfully.. ")
    return redirect('user:poll_list')


def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'user_module/poll_results.html', {
        'poll': poll
    })