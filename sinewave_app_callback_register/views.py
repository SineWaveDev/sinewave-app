from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

@api_view(['POST'])
def insert_ticket(request):
    # Get data from request
    data = request.data
    Ticket_ID = data.get('Ticket_ID')
    PROD_ID = data.get('PROD_ID')
    CUST_ID = data.get('CUST_ID')
    REQUEST = data.get('REQUEST')
    VERSION_NUMBER = data.get('VERSION_NUMBER')
    CONTACT_PERSON = data.get('CONTACT_PERSON')
    CONTACT_NO = data.get('CONTACT_NO')
    QUERY_SOURCE_ID = data.get('QUERY_SOURCE_ID')
    FILE_PATH = data.get('FILE_PATH')
    filename = data.get('filename')
    up_notice = data.get('up_notice')
    up_other = data.get('up_other')
    EMP_ID = data.get('EMP_ID')
    ADD_IN_LIBRARY = data.get('ADD_IN_LIBRARY')
    IS_PUBLISHED = data.get('IS_PUBLISHED')
    EMAIL = data.get('EMAIL')
    Book_EMPID = data.get('Book_EMPID')
    REQUEST_TYPE = data.get('REQUEST_TYPE')
    TransferEMP_ID = data.get('TransferEMP_ID')

    # Database connection
    conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
    cursor = conn.cursor()

    # SQL Query
    sql_query = """
    INSERT INTO [indiataxes_com_indiataxes].[S_CLIENT_QUERIES_TICKET] 
    ([Ticket_ID], [PROD_ID], [CUST_ID], [DATE], [QUERY], [VERSION_NUMBER], [CONTACT_PERSON], [CONTACT_INFO], [QUERY_SOURCE_ID], [STATUS], [NO_OF_QUERY], [FILE_PATH], [up_notice], [up_other], [EMP_ID], [ADD_IN_LIBRARY], [IS_PUBLISHED], [EMAIL], [BOOK_EMPID], [REQUEST_TYPE], [TRANSFER_TO_EMP_ID])
    VALUES 
    (%s, %s, %s, convert(varchar(20), getdate(), 20), %s, %s, %s, %s, %s, '2', 1, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # File paths concatenation
    file_path_concat = FILE_PATH + filename
    up_notice_concat = FILE_PATH + up_notice
    up_other_concat = FILE_PATH + up_other

    # Execute the query
    try:
        cursor.execute(sql_query, (Ticket_ID, PROD_ID, CUST_ID, '1.' + REQUEST, VERSION_NUMBER, CONTACT_PERSON, CONTACT_NO, QUERY_SOURCE_ID, file_path_concat, up_notice_concat, up_other_concat, EMP_ID, ADD_IN_LIBRARY, IS_PUBLISHED, EMAIL, Book_EMPID, REQUEST_TYPE, TransferEMP_ID))
        conn.commit()
        response_data = {"message": "Data inserted successfully"}
        return Response(response_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        conn.rollback()
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        cursor.close()
        conn.close()
