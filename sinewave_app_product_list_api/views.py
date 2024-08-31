from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql
import jwt

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'
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

@api_view(['GET'])
def get_products(request):
    # Extract the token from the Authorization header
    token = request.headers.get('Authorization')

    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Validate the token
    user_id = validate_jwt_token(token)

    if not user_id:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Connect to MSSQL database
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Execute query
        cursor.execute('SELECT PROD_ID, NAME FROM cs_product')

        # Fetch all rows
        rows = cursor.fetchall()

        # Format data into JSON response
        products = [{'PROD_ID': row[0], 'NAME': row[1]} for row in rows]

        # Close connection
        conn.close()

        # Return JSON response
        return Response(products, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
