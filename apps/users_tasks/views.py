from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import datetime

# render the login and register page
def index(request):
    return render(request, 'users_tasks/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=hash1.decode('utf-8'),
            dob=request.POST['dob']
        )
        my_user_id = User.objects.get(id=user.id)
        messages.info(request, 'You have successfully registered.')

        return redirect('/')

# login a user that is in the database
def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if 'user' in errors:
            request.session['id'] = errors['user'].id
            return redirect('/show')
        else:
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/')

# render the success file
def show(request):
    now = datetime.datetime.now()
    current_date = now.strftime('%Y-%m-%d')

    val = User.objects.get(id=request.session['id'])
    appt = Appointment.objects.filter(user_id=request.session['id']).filter(date=current_date)
    other_appointments = Appointment.objects.filter(user_id=request.session['id']).exclude(date=current_date)
    finished_tasks = Appointment.objects.filter(user_id=request.session['id']).exclude(status='pending')
    context = {
        'user':val,
        'appointment':appt,
        'other_appointments': other_appointments,
        'finished_tasks': finished_tasks
    }
    return render(request, 'users_tasks/success.html', context)

# logout the user current user
def logout(request):
    request.session.clear()
    return redirect('/')

# add an appointment to the database
def add_appt(request):
    if request.method == 'POST':
        errors = Appointment.objects.adding_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/show')
        else:
            val = User.objects.get(id=request.session['id'])
            appt = Appointment.objects.create(task=request.POST['task'], status='pending', date=request.POST['date'], time=request.POST['time'], user=val)
            return redirect('/show')

# render the edit page with a specific appointment that wants to be edited
def edit(request, appt_id):

    if "id" not in request.session:
        return redirect('/')
    else:
        appt = Appointment.objects.get(id=appt_id)
        if request.session['id'] == appt.user_id:
            context = {
                'appt_id': appt_id,
                'appt': appt
            }
            return render(request, 'users_tasks/edit.html', context)
        else:
            return redirect('/show')

# update the current appointment and redirect to the success file through show
def update(request, appt_id):
    if request.method == "POST":
        errors = Appointment.objects.adding_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/show')
        else:
            this_appt = Appointment.objects.get(id=appt_id)
            this_appt.task = request.POST['task']
            this_appt.status = request.POST['status']
            this_appt.date = request.POST['date']
            this_appt.time = request.POST['time']
            this_appt.save()
            return redirect('/show')

# delete a specified appointment
def delete(request, appt_id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        this_appt = Appointment.objects.get(id=appt_id)
        user = User.objects.get(id=request.session['id'])
        if request.session['id'] == this_appt.user_id:
            this_appt.delete()
            messages.info(request, "Your appointment has been successfully deleted, "+ user.name)
            return redirect('/show')
        else:
            messages.error(request, "You are not allowed to DELETE other's appointments, " + user.name + "!")
            return redirect('/show')
