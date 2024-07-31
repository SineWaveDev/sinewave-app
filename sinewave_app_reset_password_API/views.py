from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random


# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

class ResetPasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        cust_id = request.data.get('cust_id')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not cust_id or not otp or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP from database or cache (not implemented here)

        # Update password in database
        connection = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = connection.cursor()
        cursor.execute("UPDATE CS_CUSTOMER SET CUST_PWD=%s WHERE CUST_ID=%s", (new_password, cust_id))
        connection.commit()
        connection.close()

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
