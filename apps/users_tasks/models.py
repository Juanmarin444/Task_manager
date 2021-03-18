# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        now = datetime.datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        email = postdata["email"]
        registered_email = User.objects.filter(email=email)

        if registered_email:
            errors["email_taken"] = "An account has already been registered with this email. Please use a different email."
        if len(postdata["name"]) < 0:
            errors["name"] = "You must provide a name"
        if postdata["password"] != postdata["confirm_pw"]:
            errors["password"] = "Please confirm password"
        if len(postdata["email"]) < 0:
            errors["email"] = "You must provide an email"
        elif not EMAIL_REGEX.match(postdata["email"]):
            errors["email"] = "Invalid email given"
        if len(postdata["password"]) < 8:
            errors["password"] = "Password must to be longer"
        if len(postdata["dob"]) == 0:
            errors["dob"] = "You must provide a date of birth"
        if postdata["dob"] > current_date:
            errors["dob"] = "Invalid date of birth"
        return errors

    def login_validator(self, postdata):
        errors = {}
        email = postdata["email"]
        logged_user = User.objects.filter(email=email)

        if logged_user:
            if bcrypt.checkpw(postdata["password"].encode(), logged_user[0].password.encode()):
                errors["user"] = logged_user[0]
            else:
                errors["wrong_password"] = "Incorrect Password"
        else:
            errors["no_user"] = "Username has yet to be registered"
        return errors

    def adding_validator(self, postdata):
        errors = {}
        now = datetime.datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime("%H:%M %p")

        if len(postdata["date"]) == 0:
            errors["no_date"] = "Please provide the appointment date"
        if postdata["date"] < current_date:
            errors["invalid_date"] = "Appointment cannot be in the past"
        if postdata["date"] == current_date:
            if postdata["time"] < current_time:
                errors["invalid_time"] = "Appointment cannot be in the past (time)"
        if len(postdata['time']) < 1:
            errors["no_time"] = "Please provide the appointment time"
        return errors

class User(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Appointment(models.Model):

    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, related_name="appointments", on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
