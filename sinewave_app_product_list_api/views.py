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
def get_products(request):
    try:
        # Connect to MSSQL database
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Execute query
        cursor.execute('SELECT PROD_ID, NAME FROM cs_product')

        # Fetch all rows
        rows = cursor.fetchall()

        # Format data into JSON response
        products = [{'PROD_ID': row[0], 'NAME': row[1]} for row in rows]

        # Close connection
        conn.close()

        # Return JSON response
        return Response(products, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
