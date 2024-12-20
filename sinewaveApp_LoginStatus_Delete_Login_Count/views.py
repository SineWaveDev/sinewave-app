from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Database connection details
DB_CONFIG = {
    'server': '3.108.198.195',
    'database': 'indiataxes_com_indiataxes',
    'username': 'indiataxes_com_indiataxes',
    'password': 'SW_02ITNETCOM'
}

# Function to connect to the database
def get_db_connection():
    return pymssql.connect(
        server=DB_CONFIG['server'],
        user=DB_CONFIG['username'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

# API to delete login count
class DeleteLoginCountAPI(APIView):
    def delete(self, request, cust_id):
        try:
            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if the Cust_id exists
            cursor.execute("SELECT COUNT(*) FROM sinewaveApp_LoginStatus WHERE Cust_id = %s", (cust_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                return Response(
                    {"message": f"No records found for Cust_id: {cust_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Delete the record(s) for the provided Cust_id
            cursor.execute("DELETE FROM sinewaveApp_LoginStatus WHERE Cust_id = %s", (cust_id,))
            connection.commit()

            return Response(
                {"message": f"Login count for Cust_id {cust_id} has been deleted successfully."},
                status=status.HTTP_200_OK
            )
        except pymssql.Error as e:
            return Response(
                {"message": "Database error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Close the database connection
            if 'connection' in locals():
                connection.close()