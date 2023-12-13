from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import pytz
from datetime import datetime
from django.utils.timesince import timesince
from django.utils import timezone
from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url='login')
def index(request):
    # Query the Comment table and get all the records
    tasks = Comment.objects.all()

    if request.method == 'POST':
        events = request.POST['events']
        city = request.POST['city']

        if not events and not city:
            messages.info(request, 'Please enter both events name and location.')
        elif not events:
            messages.info(request, 'Please enter events name.')
        elif not city:
            messages.info(request, 'Please enter location.')
        else:
            total_events = get_events(events, city)

            if total_events is None:
                messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
                return redirect('index')
            elif 'errors' in total_events:
                messages.info(request, 'No results found for the entered search terms.')
                return redirect('index')
            else:
                user_list = []

            if '_embedded' in total_events and 'events' in total_events['_embedded']:
                for event in total_events['_embedded']['events']:
                    event_name = event['name']
                    venue_name = event['_embedded']['venues'][0]['name']
                    venue_address = event['_embedded']['venues'][0]['address']['line1']
                    venue_state = event['_embedded']['venues'][0]['state']['name']
                    venue_city = event['_embedded']['venues'][0]['city']['name']
                    ticket_link = event['url']
                    event_id = event['id']

                    # Call the method to get the largest image URL
                    largest_image_url = get_largest_image(event['images'])

                    if 'dateTime' in event['dates']['start']:
                        event_datetime_str = event['dates']['start']['dateTime']

                        # Convert the string to a datetime object
                        event_datetime_naive = datetime.fromisoformat(event_datetime_str.replace("Z", "+00:00"))

                        # Set the UTC timezone to the naive datetime
                        event_datetime_naive = event_datetime_naive.replace(tzinfo=pytz.utc)

                        # Convert to the user's timezone
                        user_timezone = timezone.get_current_timezone()
                        event_datetime = event_datetime_naive.astimezone(user_timezone)

                        # Format the event date and time to human-readable formats
                        formatted_event_date = event_datetime.strftime('%a, %b %d, %Y')
                        formatted_event_time = event_datetime.strftime('%I:%M %p')
                    else:
                        # Skip the event if 'dateTime' key is not present
                        continue

                        # Check if there is an image available
                    if largest_image_url:
                        # Create a new dictionary to store user details
                        user_details = {
                            'eventName': event_name,
                            'venueName': venue_name,
                            'venueAddress': venue_address,
                            'venueCity': venue_city,
                            'venueState': venue_state,
                            'ticketLink': ticket_link,
                            'imageUrl': largest_image_url,
                            'eventDate': formatted_event_date,
                            'eventTime': formatted_event_time,
                            'eventID': event_id,
                        }
                        user_list.append(user_details)

                # Calculate the total number of events
                total_nums_of_events = len(user_list)
            else:
                messages.info(request, 'No event found.')
                total_nums_of_events = 0

            # Retrieve the user's comments
            user_comments = Comment.objects.filter(user=request.user)

            context = {'events': user_list, 'total_events': total_nums_of_events, 'tasks': tasks,
                       'user_comments': user_comments}
            return render(request, 'ticketmaster/myPageTicketmaster.html', context)

    # Retrieve the user's comments if no search is performed
    user_comments = Comment.objects.filter(user=request.user)
    context = {'tasks': tasks, 'user_comments': user_comments}
    return render(request, 'ticketmaster/myPageTicketmaster.html', context)


# This Function to get the largest pic from of the event based on the height and width
def get_largest_image(images):
    # Initialize with the first image
    largest_image = None
    largest_size = images[0]['width'] * images[0]['height']

    for current_image in images[1:]:
        current_size = current_image['width'] * current_image['height']

        # Compare based on size
        if current_size > largest_size:
            largest_image = current_image['url']
            largest_size = current_size
    return largest_image


def get_events(events, city):
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
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_comments(request):
    if request.method == 'GET':
        eventID = request.GET.get('eventID')
        comments = Comment.objects.filter(eventID=eventID)

        response_data = {
            'comments': [
                {
                    'username': comment.user.username,
                    'comment': comment.comment,
                    'created_at': comment.created_at.strftime('%Y-%m-%d'),
                }
                for comment in comments
            ]
        }
    return JsonResponse(response_data)


# CRUD Operations: Create, Retrieve, Update, Delete
@login_required(login_url='login')
def create_comment(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        message = request.POST.get('message')
        eventID = request.POST.get('eventID')
        comment = Comment.objects.create(user=request.user, comment=message, eventID=eventID)

        # Calculate the time difference
        # time_since_comment = timesince(comment.created_at)
        # Return the newly created comment details
        return JsonResponse({
            'username': comment.user.username,
            'comment': comment.comment,
            'created_at': comment.created_at.strftime('%Y-%m-%d'),
        })


@login_required(login_url='login')
def update_comment(request, event_id):
    # Get the comment based on its id
    comment = Comment.objects.get(id=event_id, user=request.user)

    # if request.method == 'POST':

    return None


@login_required(login_url='login')
def delete_comment(request):
    return None


@login_required(login_url='login')
def search_comment(request):
    return None
