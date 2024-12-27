import datetime
import requests
import pymssql
from rest_framework.response import Response
from rest_framework.views import APIView


# Database connection credentials
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'
SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key


# Function to connect to the database
def get_db_connection():
    return pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)


# Function to generate the ticket ID
def fnGetQBTicketIDNo():
    # Initialize ticket ID
    functionReturnValue = ""

    # Get the current date
    today = datetime.datetime.today()
    strYYYYMM = today.strftime("%Y%m")  # YYYYMM format

    # Default maxID value
    maxID = "0"

    # Connect to the database using pymssql
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()

    # SQL query to fetch the current max ticket ID for the current month (YYYYMM)
    cursor.execute("""
        SELECT ISNULL(MAX(RIGHT(Ticket_ID, 5)), 0) AS MaxTicketId 
        FROM indiataxes_com_indiataxes.S_CLIENT_QUERIES_TICKET 
        WHERE LEFT(Ticket_ID, 6) = %s AND LEN(Ticket_ID) = 12 AND Query_Source_ID = 2
    """, (strYYYYMM,))

    # Fetch the result
    result = cursor.fetchone()

    if result and result[0] is not None:
        maxID = int(result[0]) + 1  # Increment the last maxID by 1
    else:
        maxID = 1  # If no ticket ID exists, start with 1

    # Format maxID to be 5 digits
    maxID = str(maxID).zfill(5)

    # Concatenate the final Ticket ID
    ticketID = f"{strYYYYMM}2{maxID}"

    # Close the database connection
    cursor.close()
    conn.close()

    # Return the generated ticket ID
    return ticketID


# Create the API View to handle the request
class CreateMeetingView(APIView):

    def post(self, request):
        # Step 1: Validate Input
        cust_name = request.data.get('cust_name')
        cust_monile = request.data.get('cust_monile')
        cust_id = request.data.get('cust_id')
        cust_email = request.data.get('cust_email')
        query = request.data.get('query')
        

        if not cust_name or not cust_email:
            return Response({'error': 'Customer name and email are required'}, status=400)

        # Step 2: Get access token for Microsoft Graph API
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

        # Step 3: Create the Teams Meeting
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

            # Extract the meeting URL from the appropriate fields
            join_url = event_details.get('onlineMeeting', {}).get('joinUrl') or event_details.get('onlineMeetingUrl') or event_details.get('webLink')
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to create the meeting: {str(e)}'}, status=400)

        # Step 4: Generate the Ticket ID
        ticket_id = fnGetQBTicketIDNo()
        print("Generated Ticket ID:", ticket_id)

        # Step 5: Insert Meeting Details into the Database
        try:
            emp_id = 1  # Assuming emp_id is provided or fetched based on business logic
            query = query
            status = 2
            email = cust_email  # Use the customer email as the email for the meeting
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transfer_to_emp_id = emp_id
            query_source_id = 2
            transfer_to = 0
            request_type = 'get'
            teams_emp_id = emp_id
            add_in_library = 0
            is_published = 0

            # Dynamic values for Teams URL and other fields
            Team_url = join_url

            # SQL Insert Query using parameterized query
            insert_query = """
                INSERT INTO [indiataxes_com_indiataxes].[S_CLIENT_QUERIES_TICKET]
                ([CUST_ID], [PROD_ID], [QUERY], [EMP_ID], [STATUS], [EMAIL], [DATE], 
                [Ticket_ID], [TRANSFER_TO_EMP_ID], [QUERY_SOURCE_ID], [TRANSFER_TO], 
                [REQUEST_TYPE], [WaitingUrl], [Teams_EmpId], [ADD_IN_LIBRARY], [IS_PUBLISHED], [TeamsName], [TeamsContact], [TeamsEmailid])
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            query_values = (
                cust_id, 1, query, emp_id, status, email, current_datetime,
                ticket_id, transfer_to_emp_id, query_source_id, transfer_to, 
                request_type, Team_url, teams_emp_id, add_in_library, is_published, 
                cust_name, cust_monile, cust_email
            )

            print("insert_query:",insert_query)

            # Connect to the database and execute the query
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                # Execute the parameterized query
                cursor.execute(insert_query, query_values)
                connection.commit()
                print("Meeting details successfully added to the database.")
            except pymssql.DatabaseError as e:
                print(f"Error occurred while inserting data: {str(e)}")
                return Response({'error': f'Database error: {str(e)}'}, status=500)
            finally:
                cursor.close()
                connection.close()

            return Response({
                'message': 'Meeting created successfully',
                'meeting_url': join_url,
                'attendees': event_details.get('attendees', [])
            }, status=201)

        except Exception as e:
            return Response({'error': f'Error occurred: {str(e)}'}, status=500)
