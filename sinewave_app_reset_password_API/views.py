from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
import jwt

# Database connection parameters
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

class ResetPasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the token from the Authorization header
        token = request.headers.get('Authorization')
        
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validate the token
        user_id = validate_jwt_token(token)
        
        if not user_id:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

        cust_id = request.data.get('cust_id')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not cust_id or not otp or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP from database
        connection = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CS_OTP WHERE CUST_ID=%s AND OTP=%s", (cust_id, otp))
        otp_record = cursor.fetchone()

        if not otp_record:
            connection.close()
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally, check if OTP has expired

        # Update password in database
        cursor.execute("UPDATE CS_CUSTOMER SET CUST_PWD=%s WHERE CUST_ID=%s", (new_password, cust_id))
        connection.commit()
        connection.close()

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
