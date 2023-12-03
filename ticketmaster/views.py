from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from datetime import datetime
from django.contrib import messages

import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location
        events = request.POST['events']
        city = request.POST['city']

        # Check if either events or city is empty
        if not events and not city:
            messages.info(request, 'Please enter both events name and location.')
            # redirect user to the index page
            return redirect('ticketmaster-index')

        # call function get_events() to get the data from the API
        total_events = get_events(events, city)
        print(total_events)

        # If the request to fetch data from ticketmaster was unsuccessful or returned None
        if total_events is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('ticketmaster-index')
        else:
            # Store each user's information in a variable
            users = total_events['results']

            # Initialize an empty list to store user data
            user_list = []

            for user in users:
                # Extract relevant information from the user dictionary
                venueName = user['venueName']
                venueCity = user['venueCity']
                venueState = user['venueState']
                venueAddress = user['venueAddress']
                picture = user['picture']
                ticketLink = user.url

                # Create a new dictionary to store user details
                user_details = {
                    'venueName': venueName,
                    'venueCity': venueCity,
                    'venueState': venueState,
                    'venueAddress': venueAddress,
                    'picture': picture,
                    'ticketLink': ticketLink
                }

                # Append the user details dictionary to the user_list
                user_list.append(user_details)

            # Create a context dictionary with the user_list and render the 'index.html' template
            context = {'users': user_list}
            return render(request, 'ticketmaster/myPageTicketmaster.html', context)

    # just render the page without sending/passing any context to the template It
    return render(request, 'ticketmaster/myPageTicketmaster.html')


def get_events(events, city):
    print('test')

    try:
        apikey = 'BSQwvGEqBVyuq8qtKajfgDTwfuufWVUX'
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "classificationName": events,
            "city": city,
            "sort": "date,asc",
            "apikey": apikey
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None



### pip3 install numpy
### pip3 install matplotlib
def plotit():
    x = np.random.randn(1000)
    plt.hist(x, bins=20)
    plt.show()

    plt.hist(x, bins=range(-4, 5))
    plt.show()

    plt.hist(x, bins=20, histtype='step', linewidth=2)
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8)
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8, edgecolor='darkgreen')
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8, edgecolor='red')
    plt.show()

    plt.hist(x, bins=20, rwidth=0.7, edgecolor='red')
    plt.savefig('static/ourDjangoPlot.png')
    ### plt.show()

# // In jQuery
# $("#imageContainer").html('<img src="plot.png">');

plotit()
