from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, "index.html")


def wall(request):

    if 'emails' not in request.session:
        return redirect("/")

    context = {
        'user': User.objects.get(email=request.session['emails']),
        'posted_msg': Message.objects.all(),
    }

    return render(request, "wall.html", context)


# *******************************************************************************


def register(request):
    errors = User.objects.new_user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("Not registered*****")
            return redirect("/")

    else:
        hashed_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hashed_password', "******")
        created_user = User.objects.create(
            email=request.POST['emails'],
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            password=hashed_password,
        )

    request.session['emails'] = created_user.email
    print("New user is registered*****")
    print(request.POST)
    return redirect("/wall")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    request.session['emails'] = request.POST['emails']
    return redirect("/wall")


def logout(request):
    request.session.clear()
    return redirect("/")


def post_new_msg(request):

    current_user = User.objects.get(email=request.session['emails'])

    Message.objects.create(
        message=request.POST['new_message'],
        user=current_user,
    )

    print("Message posted! *********")
    print(request.POST, '*********')
    return redirect("/wall")


def post_new_comment(request):

    current_user = User.objects.get(email=request.session['emails'])
    message_to_comment = Message.objects.get(id=request.POST['post_id'])

    Comment.objects.create(
        comment=request.POST['new_comment'],
        user=current_user,
        message=message_to_comment,
    )

    print("Comment posted! *********")
    print(request.POST, '*********')
    return redirect("/wall")
