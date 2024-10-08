from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql
import jwt
from datetime import datetime

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

# JWT Secret Key
SECRET_KEY = 'your_secret_key'  # Replace with your actual secret key

def validate_jwt_token(token):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']  # Assuming the token payload includes the user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@api_view(['POST'])
def get_webinar_details(request):
    # Extract token from the Authorization header
    token = request.headers.get('Authorization')
    
    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Validate the token
    user_id = validate_jwt_token(token)
    
    if not user_id:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

    # Extract date parameters from the request body
    start_date = request.data.get('startDate')
    end_date = request.data.get('endDate')

    # Validate date format
    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Connect to the database
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor(as_dict=True)

        # Construct the SQL query
        query = 'SELECT * FROM SINEWAVE_WEBINAR_MASTER WHERE 1=1'
        params = ()

        if start_date:
            query += ' AND webinar_date >= %s'
            params += (start_date,)  # Add the start date to the tuple
        if end_date:
            query += ' AND webinar_date <= %s'
            params += (end_date,)  # Add the end date to the tuple

        # Execute the query with parameters
        cursor.execute(query, params)

        # Fetch all results
        results = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the results in the response
        return Response(results, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
