from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://7dc9cbcd.us-south.apigw.appdomain.cloud/capstone/get_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = "https://7dc9cbcd.us-south.apigw.appdomain.cloud/capstone/reviews"
    context = {}
    params=dict()
    params["dealership"] = dealer_id
    dealer_details = get_dealer_reviews_from_cf(url,kwargs=params)
    context["dealer_details"] = dealer_details
    context["dealer_id"] = dealer_id
    context["dealer_name"] = get_dealers_from_cf("https://7dc9cbcd.us-south.apigw.appdomain.cloud/capstone/get_dealerships")[dealer_id-1].full_name
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    url = "https://7dc9cbcd.us-south.apigw.appdomain.cloud/capstone/reviews"
    if request.method == 'GET':
        url = "https://7dc9cbcd.us-south.apigw.appdomain.cloud/capstone/get_dealerships"
        context = {}
        context["dealer_id"] = dealer_id
        context["dealer_name"] = get_dealers_from_cf(url)[dealer_id].full_name
        context["cars"]=CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            if review["purchase"] == True:
                car=request.POST["car"].split(",")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car[0]
                review["car_model"]=car[1]
                review["car_year"]=car[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None

            json_payload = dict()
            json_payload["review"] = review
            result = post_request(url, json_payload, dealerId=dealer_id)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    


