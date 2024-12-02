import random
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ScheduleMeeting(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get customer name and email from the request
        cust_name = request.data.get('cust_name')
        cust_email = request.data.get('cust_email')

        if not cust_name or not cust_email:
            return Response({'error': 'Customer name and email are required'}, status=400)

        # Step 1: Get the access token using client credentials
        token_url = "https://login.microsoftonline.com/f63f8f14-9b26-4bd7-8ccb-4dfd683a99bf/oauth2/v2.0/token"
        client_credentials = {
            'grant_type': 'client_credentials',
            'client_id': '363bfc81-18f6-4356-a60d-38f32c1db037',
            'client_secret': 'aGQ8Q~9Hwopkz45c_juetCOVS1XlHRVr7f3Z3bSX',
            'scope': 'https://graph.microsoft.com/.default',
        }

        try:
            token_response = requests.post(token_url, data=client_credentials)
            token_response.raise_for_status()
            access_token = token_response.json().get('access_token')
            print("Access Token:", access_token)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to get access token: {str(e)}'}, status=400)

        # Step 2: Check the presence of users
        users = {
            "sagar.p@sinewave.in": "1f9caece-f785-4f51-9344-4e495f157275",
            "girish.d@sinewave.in": "10d5a857-ab3d-470f-ae6d-23aaec6db8de",
            "nasir.s@sinewave.in": "716a553a-5013-4a36-bdb5-36754196af78",
        }

        available_users = []
        for email, object_id in users.items():
            presence_url = f"https://graph.microsoft.com/v1.0/users/{object_id}/presence"
            headers = {'Authorization': f'Bearer {access_token}'}

            try:
                presence_response = requests.get(presence_url, headers=headers)
                presence_response.raise_for_status()
                presence_data = presence_response.json()

                if presence_data.get('availability') == 'Available' and presence_data.get('activity') == 'Available':
                    available_users.append({'email': email, 'object_id': object_id})
            except requests.exceptions.RequestException as e:
                print(f"Failed to check presence for {email}: {str(e)}")

        # Step 3: Check if there are any available users
        if not available_users:
            return Response({'error': 'All executives are busy. Please try again later or register for a call back.'}, status=400)

        # Step 4: Randomly pick an available user
        selected_user = random.choice(available_users)
        print("Selected user:", selected_user)

        # Step 5: Create an event (meeting) for the selected user
        event_url = "https://graph.microsoft.com/v1.0/users/admin@sinewave.in/events"
        event_data = {
            "subject": "Team Sync Meeting",
            "start": {
                "dateTime": "2024-11-22T15:00:00",
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": "2024-11-22T16:00:00",
                "timeZone": "UTC"
            },
            "attendees": [
                {
                    "emailAddress": {
                        "address": cust_email,
                        "name": cust_name,
                    },
                    "type": "required"
                },
                {
                    "emailAddress": {
                        "address": selected_user['email'],
                        "name": selected_user['email'].split('@')[0]  # Use the part before '@' as the name
                    },
                    "type": "required"
                }
            ],
            "location": {
                "displayName": "Online"
            },
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness",
            "body": {
                "contentType": "HTML",
                "content": "Please join the meeting through Microsoft Teams."
            }
        }

        event_headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

       
        try:
            event_response = requests.post(event_url, json=event_data, headers=event_headers)
            event_response.raise_for_status()  # Raise error for bad status codes
            event_details = event_response.json()
            attendees = event_details.get('attendees')
            online_meeting_url = event_details.get('onlineMeetingUrl')
            if not online_meeting_url:
                online_meeting_url = event_details.get('webLink')  # Fallback to web link if no online meeting URL

            if not attendees:
                attendees = event_details.get('webLink')  # Fallback to web link if no online meeting URL

            return Response({
                'message': 'Meeting created successfully',
                'attendees' : attendees,
                'meeting_url': online_meeting_url
            }, status=201)

        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to create the meeting: {str(e)}'}, status=400)


