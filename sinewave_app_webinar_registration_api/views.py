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
def add_webinar(request):
    data = request.data
    cust_id = data.get('cust_id')
    cust_pwd = data.get('cust_pwd')
    webinar_subject = data.get('webinar_subject')
    webinar_date = data.get('webinar_date')
    webinar_time = data.get('webinar_time')
    webinar_url = data.get('webinar_url')
    webinar_type = data.get('webinar_type')

    try:
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Verify customer ID and password
        verify_query = "SELECT COUNT(*) FROM CS_CUSTOMER WHERE CUST_ID = %s AND CUST_PWD = %s"
        cursor.execute(verify_query, (cust_id, cust_pwd))
        if cursor.fetchone()[0] == 0:
            return Response({"error": "Invalid customer ID or password"}, status=status.HTTP_400_BAD_REQUEST)

        insert_query = """
        INSERT INTO SINEWAVE_WEBINAR_MASTER (WEBINAR_SUBJECT, WEBINAR_DATE, WEBINAR_TIME, WEBINAR_URL, WEBINAR_TYPE)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (webinar_subject, webinar_date, webinar_time, webinar_url, webinar_type))
        conn.commit()
        conn.close()

        return Response({"message": "Webinar added successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
