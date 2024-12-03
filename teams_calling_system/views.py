import random
import requests
import pymssql
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime

# Database connection credentials
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'
SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key


# Function to connect to the database
def get_db_connection():
    return pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)


# Custom Authentication Class
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        return (payload, None)


class ScheduleMeeting(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        # Step 1: Validate Input
        cust_name = request.data.get('cust_name')
        cust_email = request.data.get('cust_email')

        if not cust_name or not cust_email:
            return Response({'error': 'Customer name and email are required'}, status=400)

        # Step 2: Get access token
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
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to get access token: {str(e)}'}, status=400)

        # Step 3: Fetch employees from the database
        query = """
            SELECT NEW_EMP_ID, F_NAME + L_NAME AS Name, EMAIL
            FROM CS_EMPLOYEE
            WHERE DISCONTINUE='0' AND DEPARTMENT='10' AND TEAM='C' AND EMP_ID != '100202'
        """

        try:
            connection = get_db_connection()
            cursor = connection.cursor(as_dict=True)
            cursor.execute(query)
            employees = cursor.fetchall()
        except pymssql.DatabaseError as e:
            return Response({'error': f'Database error: {str(e)}'}, status=500)
        finally:
            connection.close()

        # Step 4: Get object IDs for employees
        employee_data = {}
        print("all_data:", employee_data)
        for employee in employees:
            email = employee['EMAIL']
            print("Email_ID:", email) 
            user_url = f"https://graph.microsoft.com/v1.0/users/{email}"
            headers = {'Authorization': f'Bearer {access_token}'}

            try:
                user_response = requests.get(user_url, headers=headers)
                user_response.raise_for_status()
                user_data = user_response.json()
                print("user_data:", user_data)
                employee_data[email] = {
                    'id': user_data['id'],
                    'name': employee['Name']
                }
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch object ID for {email}: {str(e)}")

        # Step 5: Check user presence
        available_users = []
        
        for email, data in employee_data.items():
            print("available:", data['id'])
            presence_url = f"https://graph.microsoft.com/v1.0/users/{data['id']}/presence"
            headers = {'Authorization': f'Bearer {access_token}'}

            try:
                presence_response = requests.get(presence_url, headers=headers)
                presence_response.raise_for_status()
                presence_data = presence_response.json()

                if presence_data.get('availability') == 'Available' and presence_data.get('activity') == 'Available':
                    available_users.append({'email': email, 'object_id': data['id'], 'name': data['name']})
            except requests.exceptions.RequestException as e:
                print(f"Failed to check presence for {email}: {str(e)}")
        print("available_users:", available_users)
        if not available_users:
            return Response({'error': 'All executives are busy. Please try again later or register for a call back.'}, status=400)

        # Step 6: Create the meeting
        selected_user = random.choice(available_users)
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

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            event_response = requests.post(event_url, json=event_data, headers=headers)
            event_response.raise_for_status()
            event_details = event_response.json()
            print("event_details:", event_details)

            # Extract the meeting URL from the appropriate fields
            join_url = event_details.get('onlineMeeting', {}).get('joinUrl') or event_details.get('onlineMeetingUrl') or event_details.get('webLink')

            return Response({
                'message': 'Meeting created successfully',
                'meeting_url': join_url,  # Ensure this field correctly retrieves the join URL
                'attendees': event_details.get('attendees'),
                'selected_executive': {
                    'email': selected_user['email'],
                    'name': selected_user['name'],
                    'object_id': selected_user['object_id'],
                }
            }, status=201)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to create the meeting: {str(e)}'}, status=400)

