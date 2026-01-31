from django.shortcuts import render, redirect
from user_module.models import Poll, Option, Vote, Feedback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_module.models import Option, Vote
from django.contrib.auth import logout
from django.contrib import messages
from user_module.models import Poll, Vote, Feedback
@login_required
def dashboard_view(request):
    total_polls = Poll.objects.count()
    total_votes = Vote.objects.count()
    total_feedbacks = Feedback.objects.count()  

    context = {
        'total_polls': total_polls,
        'total_votes': total_votes,
        'total_feedbacks': total_feedbacks,  
    }
    return render(request, 'admin_module/dashboard.html', context)


def poll_list_admin(request):
    polls = Poll.objects.all()
    return render(request, 'admin_module/poll_list.html', {'polls': polls})


def add_poll(request):
    if request.method == "POST":
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')

        if question and option1 and option2:
            poll = Poll.objects.create(question=question)

            Option.objects.create(poll=poll, text=option1)
            Option.objects.create(poll=poll, text=option2)
            if option3:
                Option.objects.create(poll=poll, text=option3)
            if option4:
                Option.objects.create(poll=poll, text=option4)

            return redirect('admin_module:poll_list')

    return render(request, 'admin_module/add_poll.html')


def vote_list(request):
    votes = Vote.objects.select_related('poll', 'option', 'user').order_by('-id')
    return render(request, 'admin_module/vote_list.html', {'votes': votes})


def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_module/feedback_list.html', {'feedbacks': feedbacks})
def index(request):
    return render(request, 'user_module/index.html')


def edit_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    options = poll.options.all()  
    if request.method == "POST":
        poll.question = request.POST.get("question")
        poll.save()

    
        for idx, option in enumerate(options, start=1):
            option_text = request.POST.get(f"option{idx}")
            if option_text:
                option.text = option_text
                option.save()

       
        for i in range(len(options)+1, 5):
            new_option_text = request.POST.get(f"option{i}")
            if new_option_text:
                Option.objects.create(poll=poll, text=new_option_text)

        return redirect('admin_module:poll_list')

   
    optional_range = range(len(options)+1, 5)  
    return render(request, 'admin_module/edit_poll.html', {
        'poll': poll,
        'options': options,
        'optional_range': optional_range
    })


def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return redirect('admin_module:poll_list')


def admin_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_type == "admin":   
                login(request, user)
                return redirect("admin_module:dashboard")
            else:
                error = "You are not an admin."
        else:
            error = "Invalid username or password."

    return render(request, "admin_module/admin_login.html", {"error": error})



def admin_logout(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('admin_module:admin_login')
