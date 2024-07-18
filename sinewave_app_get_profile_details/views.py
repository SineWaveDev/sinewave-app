# views.py
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
def get_customer_details(request):
    cust_id = request.query_params.get('cust_id')
    cust_pwd = request.query_params.get('cust_pwd')
    
    if not cust_id or not cust_pwd:
        return Response({"error": "cust_id and cust_pwd are required parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        connection = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = connection.cursor(as_dict=True)
        
        query = f"SELECT * FROM CS_CUSTOMER WHERE CUST_ID = '{cust_id}' AND CUST_PWD = '{cust_pwd}'"
        cursor.execute(query)
        result = cursor.fetchone()

        connection.close()

        if result:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
