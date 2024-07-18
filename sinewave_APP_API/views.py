from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

def get_db_connection():
    return pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)

@api_view(['POST'])
def check_credentials(request):
    user_id = request.data.get('user_id')
    user_pwd = request.data.get('user_pwd')

    if not user_id or not user_pwd:
        return Response({"status": False, "error": "User ID and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        connection = get_db_connection()
        cursor = connection.cursor(as_dict=True)
        
        # Authenticate user
        query = "SELECT CUST_ID, CUST_PWD FROM CS_CUSTOMER WHERE CUST_ID = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user and user['CUST_PWD'] == user_pwd:
            # Fetch data from other tables
            cursor.execute("SELECT TOP 1 * FROM CS_CUSTOMER WHERE CUST_ID = %s", (user_id,))
            customer_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_CUSTOMER_DET WHERE CUST_ID = %s", (user_id,))
            customer_det_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_CUST_PROD WHERE CUST_ID = %s", (user_id,))
            customer_prod_data = cursor.fetchone()
            
            cursor.execute("SELECT TOP 1 * FROM CS_LICENSE_SNVW WHERE CUST_ID = %s", (user_id,))
            license_data = cursor.fetchone()
            
            response_data = {
                "status": True,
                "customer_data": customer_data,
                "customer_det_data": customer_det_data,
                "customer_prod_data": customer_prod_data,
                "license_data": license_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "error": "Incorrect user ID or password."}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        cursor.close()
        connection.close()
