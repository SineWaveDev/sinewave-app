from django.http import JsonResponse
from rest_framework.decorators import api_view
import pymssql

@api_view(['DELETE'])
def delete_user_reward_transaction(request):
    try:
        # Getting user_id from query parameters
        user_id = request.GET.get('user_id')

        # If user_id is not provided in query parameters, return an error response
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'user_id is required in query parameters.'}, status=400)

        # Database connection parameters
        SERVER = '3.108.198.195'
        DATABASE = 'indiataxes_com_indiataxes'
        USERNAME = 'indiataxes_com_indiataxes'
        PASSWORD = 'SW_02ITNETCOM'

        # Establishing connection to SQL Server
        conn = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = conn.cursor()

        # SQL Query to delete the record for the given user_id
        delete_query = "DELETE FROM UserRewardTransactions WHERE user_id = %s"

        # Executing the query
        cursor.execute(delete_query, (user_id,))
        conn.commit()

        # Closing the connection
        cursor.close()
        conn.close()

        # Returning success response
        return JsonResponse({'status': 'success', 'message': f'Record with user_id {user_id} deleted successfully.'}, status=200)
    
    except Exception as e:
        # Handling errors and returning failure response
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
