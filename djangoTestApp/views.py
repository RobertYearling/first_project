from django.shortcuts import render, redirect, HttpResponse # HttpResponse and redirect are needed
from django.contrib import messages
from .models import *


# Create your views here.

def main(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registerValidation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        newUser = User.objects.create(f_name = request.POST['f_name'], l_name = request.POST['l_name'], email = request.POST['email'], password = request.POST['pswd'])
        request.session['logInId'] = newUser.id
    return redirect('/travels')

def login(request):
    errors = User.objects.loginValidation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        userEmail = User.objects.filter(email = request.POST['email'])
        request.session['logInId'] = userEmail[0].id
    return redirect('/travels')


def travels(request):
    context = {
        'userLog' : User.objects.get(id=request.session['logInId']),
        'allTrips' : Planner.objects.filter(planner=User.objects.get(id=request.session['logInId'])),
        'myTrips' : Planner.objects.filter(joining=User.objects.get(id=request.session['logInId'])),
        'otherTrips' : Planner.objects.exclude(joining=User.objects.get(id=request.session['logInId'])),
    }
    return render(request, 'travels.html', context)

def view(request, tripId):
    context = {
        'trips' : Planner.objects.get(id=tripId),
        'join' : Planner.objects.get(id=tripId)
    }
    return render(request, 'view.html', context)

def createTrip(request):
    return render(request, 'addtrip.html')

def addTrip(request):
    errors = Planner.objects.planValidation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/createTrip')
    else:
        Planner.objects.create(destination = request.POST['dest'], decription = request.POST['desc'], planner = User.objects.get(id=request.session['logInId']), travel_from = request.POST['travel_from'], travel_to = request.POST['travel_to'])
    return redirect('/travels')

def addToTrip(request, tripId):
    Planner.objects.get(id=tripId).joining.add(User.objects.get(id=request.session['logInId'])),
    return redirect('/travels')

def cancelTrip(request, tripId):
    Planner.objects.get(id=tripId).joining.remove(User.objects.get(id=request.session['logInId']))
    return redirect('/travels')

def deleteTrip(request, tripId):
    Planner.objects.get(id=tripId).delete()
    return redirect('/travels')

def back(request):
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')