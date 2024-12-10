from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql
import jwt
import datetime

print("login api working")

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'
SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key

def get_db_connection():
    return pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)

def generate_jwt_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({'user_id': user_id, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    return token

def validate_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@api_view(['POST'])
def check_credentials(request):
    user_id = request.data.get('user_id')
    user_pwd = request.data.get('user_pwd')
    token = request.headers.get('Authorization')

    if token:
        # Validate existing token
        user_id_from_token = validate_jwt_token(token)
        if user_id_from_token:
            return Response({"status": True, "message": "User is still logged in."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "error": "Session expired. Please log in again."}, status=status.HTTP_401_UNAUTHORIZED)

    if not user_id or not user_pwd:
        return Response({"status": False, "error": "User ID and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        connection = get_db_connection()
        cursor = connection.cursor(as_dict=True)
        
        # Authenticate user
        query = "SELECT CUST_ID, CUST_PWD FROM CS_CUSTOMER WHERE CUST_ID = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user and user['CUST_PWD'] == user_pwd:
            # Generate a new token
            token = generate_jwt_token(user_id)

            # Fetch data from other tables
            cursor.execute("SELECT TOP 1 * FROM CS_CUSTOMER WHERE CUST_ID = %s", (user_id,))
            customer_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_CUSTOMER_DET WHERE CUST_ID = %s", (user_id,))
            customer_det_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_CUST_PROD WHERE CUST_ID = %s", (user_id,))
            customer_prod_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_LICENSE_SNVW WHERE CUST_ID = %s", (user_id,))
            license_data = cursor.fetchone()

            # # Fetch the coin balance from UserRewardTransactions table
            # cursor.execute("SELECT SUM(transactionType) AS coin_balance FROM UserRewardTransactions WHERE userId = %s", (user_id,))
            # coin_balance_data = cursor.fetchone()
            # coin_balance = coin_balance_data['coin_balance'] if coin_balance_data else 0

            response_data = {
                "status": True,
                "token": token,
                "customer_data": customer_data,
                "customer_det_data": customer_det_data,
                "customer_prod_data": customer_prod_data,
                "license_data": license_data,
                # "coin_balance": coin_balance  # Include the coin balance in the response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "error": "Incorrect user ID or password."}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        cursor.close()
        connection.close()
