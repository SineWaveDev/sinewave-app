from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
from datetime import datetime, timedelta

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'


class VerifyOTPAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cust_id = request.data.get('cust_id')
            otp = request.data.get('otp')

            if not cust_id or not otp:
                return Response({"error": "Customer ID and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify OTP from database
            try:
                connection = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
                cursor = connection.cursor(as_dict=True)
                cursor.execute("SELECT TOP 1 OTP, TIMESTAMP FROM CS_OTP WHERE CUST_ID=%s ORDER BY TIMESTAMP DESC", (cust_id,))
                result = cursor.fetchone()
                connection.close()
            except pymssql.Error as db_err:
                print(f"Database error: {db_err}")
                return Response({"error": "Database connection error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            print("result:", result)

            if not result:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            db_otp = str(result['OTP'])  # Convert database OTP to string
            otp_timestamp = result['TIMESTAMP']
            current_time = datetime.now()

            if db_otp == str(otp):  # Convert request OTP to string and compare
                if current_time - otp_timestamp > timedelta(minutes=2):
                    return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
