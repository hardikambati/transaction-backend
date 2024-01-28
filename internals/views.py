from django.db.models import Q
from rest_framework import (
    views,
    response,
    status,
)

# custom
from . import decorators
from transactions import utility
from utils.config import TRANSACTION_STATUS
from transactions import models as core_models
from transactions import serializers as core_serializers
from websockets.utility import send_message_to_channel


class TransactionStatusAPIView(views.APIView):

    model_class      = core_models.Transaction
    serializer_class = core_serializers.TransactionSerializer

    @decorators.authenticate_service
    @decorators.validate_signature
    def post(self, request, *args, **kwargs):
        '''
        consumes data sent by MS
        if it's a success message - changes status of transaction
        if it's an error message  - creates a log in metadata of transaction
        '''

        data = request.data
        txn_pk = kwargs.get('id')
        txn_id = kwargs.get('txn_id')

        transaction = self.model_class.objects.filter(
            Q(id=txn_pk) &
            Q(txn_id=txn_id)
        )

        if not transaction.exists():
            return response.Response(
                {'detail': 'Invalid transaction info'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # fetch status
        try:
            txn_status = data['payload']['extra_data']['status']
            if not txn_status in TRANSACTION_STATUS:
                raise Exception('Invalid status received')
        except:
            return response.Response(
                {'detail': 'Invalid status received'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # fetch user id
        try:
            user_id = data['payload']['data']['user']
        except:
            return response.Response(
                {'detail': 'Invalid user id received'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = transaction.first()

        error = data['payload']['extra_data'].get('log', None)
        if error:
            # create error log
            utility.create_transaction_log(transaction_instance=transaction, error=error)
        else:
            send_message_to_channel(user_id=user_id, message={'status': txn_status})
            transaction.status = txn_status
            transaction.save()

        serializer = self.serializer_class(transaction, many=False)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
