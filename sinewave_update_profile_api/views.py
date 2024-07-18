from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

@api_view(['POST'])
def update_customer(request):
    data = request.data
    cust_id = data.get('cust_id')
    cust_pwd = data.get('cust_pwd')
    fields_to_update = {}

    if data.get('name'):
        fields_to_update['NAME'] = data.get('name')
    if data.get('add1'):
        fields_to_update['ADD1'] = data.get('add1')
    if data.get('add2'):
        fields_to_update['ADD2'] = data.get('add2')
    if data.get('city'):
        fields_to_update['CITY'] = data.get('city')
    if data.get('state'):
        fields_to_update['STATE'] = data.get('state')
    if data.get('pin'):
        fields_to_update['PIN'] = data.get('pin')
    if data.get('email'):
        fields_to_update['Email'] = data.get('email')
    if data.get('gstn_no'):
        fields_to_update['GSTN_NO'] = data.get('gstn_no')

    if not fields_to_update:
        return Response({"error": "No fields to update"}, status=status.HTTP_400_BAD_REQUEST)

    set_clause = ", ".join(f"{key} = %s" for key in fields_to_update.keys())
    values = tuple(fields_to_update.values()) + (cust_id, cust_pwd)

    try:
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        query = f"""
        UPDATE CS_CUSTOMER
        SET {set_clause}
        WHERE CUST_ID = %s AND CUST_PWD = %s
        """
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return Response({"message": "Customer details updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
