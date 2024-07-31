from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from datetime import datetime

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_username = "crm@sinewave.co.in"
email_password = "fzjv eaaj kdcv svqr"

class RequestOTPAPI(APIView):
    def post(self, request, *args, **kwargs):
        cust_id = request.data.get('cust_id')

        if not cust_id:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get email from database
        connection = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = connection.cursor(as_dict=True)
        cursor.execute("SELECT Email FROM CS_CUSTOMER WHERE CUST_ID=%s", (cust_id,))
        result = cursor.fetchone()

        if not result:
            connection.close()
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        email = result['Email']

        # Generate OTP
        otp = random.randint(100000, 999999)
        timestamp = datetime.now()

        # Save OTP to database
        cursor.execute("INSERT INTO CS_OTP (CUST_ID, OTP, TIMESTAMP) VALUES (%s, %s, %s)", (cust_id, otp, timestamp))
        connection.commit()
        connection.close()

        # Send OTP email
        subject = "Your OTP for Password Reset"
        body = (
            f"Dear Customer,\n\n"
            f"Your OTP for password reset is {otp}. It is valid for 2 minutes.\n\n"
            f"Please do not share this OTP with anyone.\n\n"
            f"Thank you,\n"
            f"Sinewave Computer Services Pvt. Ltd"
        )
        message = MIMEMultipart()
        message["From"] = email_username
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_username, email_password)
                server.sendmail(email_username, [email], message.as_string())
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
