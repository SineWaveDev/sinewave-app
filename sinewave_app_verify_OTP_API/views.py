from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
from datetime import datetime, timedelta
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

class VerifyOTPAPI(APIView):
    def post(self, request, *args, **kwargs):
        logger.debug("Received request data: %s", request.data)

        cust_id = request.data.get('cust_id')
        otp = request.data.get('otp')

        if not cust_id or not otp:
            logger.warning("Customer ID or OTP is missing")
            return Response({"error": "Customer ID and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify OTP from database
            with pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE) as connection:
                with connection.cursor(as_dict=True) as cursor:
                    cursor.execute("SELECT OTP, TIMESTAMP FROM CS_OTP WHERE CUST_ID=%s ORDER BY TIMESTAMP DESC", (cust_id,))
                    result = cursor.fetchone()

                    if not result:
                        logger.warning("No OTP found for the given Customer ID")
                        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

                    db_otp = str(result['OTP'])  # Convert database OTP to string
                    otp_timestamp = result['TIMESTAMP']
                    current_time = datetime.now()

                    logger.debug("db_otp: %s, otp: %s, otp_timestamp: %s, current_time: %s", db_otp, otp, otp_timestamp, current_time)

                    if db_otp == str(otp):  # Convert request OTP to string and compare
                        if current_time - otp_timestamp > timedelta(minutes=2):
                            logger.warning("OTP has expired")
                            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            logger.info("OTP verified successfully")
                            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
                    else:
                        logger.warning("Invalid OTP provided")
                        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except pymssql.DatabaseError as db_err:
            logger.error(f"Database error: {db_err}")
            return Response({"error": "Database connection error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
