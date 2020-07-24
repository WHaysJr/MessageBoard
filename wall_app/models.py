from django.db import models

import re

import bcrypt


class UserManager(models.Manager):
    def new_user_validator(self, post_data):
        errors = {}
        potential_user_list = User.objects.filter(email=post_data['emails'])
        if len(potential_user_list) > 0:
            errors['emails'] = 'A user with this email already exists'
            return errors

        if len(post_data['fname']) < 3:
            errors['fname'] = 'First name is 2Short'
        if len(post_data['lname']) < 3:
            errors['lname'] = 'Last name is 2Short'
        if len(post_data['emails']) < 3:
            errors['emails'] = 'Email is 2Short'

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(post_data['emails']):
            errors['emails'] = 'Invalid email address'
        elif len(post_data['password']) < 3:
            errors['password'] = 'Password is 2Short'
        elif (post_data['password'] != post_data['password_confirm']):
            errors['password_confirm'] = 'Password does not match'
        return errors

    def login_validator(self, post_data):
        errors = {}

        potential_user_list = User.objects.filter(email=post_data['emails'])
        if len(potential_user_list) == 0:
            errors['emails'] = 'That email does not exist'
        return errors

        does_password_match = bcrypt.checkpw(
            post_data['password'].encode(), potential_user_list[0].password.encode())

        if not does_password_match:
            errors['password'] = 'That password does not match'
        return errors


class User(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        User, related_name='user_comments', on_delete=models.CASCADE)
    message = models.ForeignKey(
        Message, related_name='message_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
