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
def get_customer_details(request):
    # Extract the token from the Authorization header
    token = request.headers.get('Authorization')

    if not token:
        return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Validate the token
    user_id = validate_jwt_token(token)

    if not user_id:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

    # Extract query parameters
    cust_id = request.query_params.get('cust_id')
    cust_pwd = request.query_params.get('cust_pwd')
    
    if not cust_id or not cust_pwd:
        return Response({"error": "cust_id and cust_pwd are required parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        connection = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = connection.cursor(as_dict=True)
        
        query = f"SELECT * FROM CS_CUSTOMER WHERE CUST_ID = '{cust_id}' AND CUST_PWD = '{cust_pwd}'"
        cursor.execute(query)
        result = cursor.fetchone()

        connection.close()

        if result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
