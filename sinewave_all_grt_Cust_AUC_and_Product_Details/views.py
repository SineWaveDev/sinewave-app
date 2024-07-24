from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

@api_view(['GET'])
def get_customer_data(request, cust_id):
    try:
        # Establish a connection to the SQL Server
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor(as_dict=True)

        # Execute the first query
        cursor.execute("SELECT * FROM CS_CUST_PROD WHERE CUST_ID = %s", (cust_id,))
        cs_cust_prod_data = cursor.fetchall()

        # Execute the second query
        cursor.execute("SELECT * FROM OS_DATA WHERE CUST_ID = %s", (cust_id,))
        os_data = cursor.fetchall()

        # Close the connection
        conn.close()

        # Create the response data
        response_data = {
            'CS_CUST_PROD': cs_cust_prod_data,
            'OS_DATA': os_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    except pymssql.DatabaseError as e:
        # Handle any database errors
        error_msg = str(e)
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        # Handle any other exceptions
        error_msg = str(e)
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
