from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from datetime import datetime
from django.contrib import messages
from datetime import datetime


# Create your views here.
def index(request):
    if request.method == 'POST':
        events = request.POST['events']
        city = request.POST['city']

        if not events and not city:
            messages.info(request, 'Please enter both events name and location.')
            return redirect('ticketmaster-index')

        total_events = get_events(events, city)

        if total_events is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            return redirect('ticketmaster-index')
        elif 'errors' in total_events:
            messages.info(request, 'No results found for the entered search terms.')
            return redirect('ticketmaster-index')
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

                    # Call the method to get the largest image URL
                    largest_image_url = get_largest_image(event['images'])

                    if 'dateTime' in event['dates']['start']:
                        event_datetime_str = event['dates']['start']['dateTime']
                        event_datetime = datetime.fromisoformat(event_datetime_str.replace("Z", "+00:00"))

                        # Format the event date and time to human-readable formats
                        formatted_event_date = event_datetime.strftime('%a, %b %d, %Y')
                        formatted_event_time = event_datetime.strftime('%I:%M %p')
                    else:
                        # Handle the case where 'dateTime' key is not present
                        registration_date = "Date not available"
                        formatted_event_time = "Time not available"

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
                    }
                    user_list.append(user_details)

                # Calculate the total number of events
                total_nums_of_events = len(user_list)
            else:
                messages.info(request, 'No event found.')
                total_nums_of_events = 0

            context = {'users': user_list, 'total_events': total_nums_of_events}
            return render(request, 'ticketmaster/myPageTicketmaster.html', context)
    return render(request, 'ticketmaster/myPageTicketmaster.html')


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
