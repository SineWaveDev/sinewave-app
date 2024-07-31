from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from datetime import datetime, timedelta

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'


class VerifyOTPAPI(APIView):
    def post(self, request, *args, **kwargs):
        cust_id = request.data.get('cust_id')
        otp = request.data.get('otp')

        if not cust_id or not otp:
            return Response({"error": "Customer ID and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify OTP from database
        connection = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = connection.cursor(as_dict=True)
        cursor.execute("SELECT OTP, TIMESTAMP FROM CS_OTP WHERE CUST_ID=%s", (cust_id,))
        result = cursor.fetchone()
        connection.close()

        if not result or str(result['OTP']) != str(otp):
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        otp_timestamp = result['TIMESTAMP']
        current_time = datetime.now()

        if current_time - otp_timestamp > timedelta(minutes=2):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming OTP verification is successful
        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
