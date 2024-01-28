from django.db.models import Q
from rest_framework import (
    response,
    status,
)

# custom
from utils.helpers import (
    request_from_args,
    decode_data,
)
from accounts import models as accounts_models


def authenticate_service(func):
    def check(*args, **kwargs):
        '''
        checks whether service is genuine or not
        updates kwargs with
        - token
        '''
        request = request_from_args(args)
        header_token = request.headers.get('MS_ACCESS_KEY')

        if not header_token:
            return response.Response(
                {'detail': 'MS_ACCESS_KEY not passed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = accounts_models.AccessToken.objects.filter(
            Q(value=header_token) &
            Q(is_active=True)
        )

        if not token.exists():
            return response.Response(
                {'detail': 'Invalid MS_ACCESS_KEY'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        kwargs.update({
            'token': token.first()
        })
        return func(*args, **kwargs)
    return check


def validate_signature(func):
    def check(*args, **kwargs):
        '''
        checks whether data sent by MS is tampered or not
        updates kwargs with
        - id
        - txn_id
        '''
        request = request_from_args(args)
        data = request.data

        try:
            # decrypt signature
            raw_signature = data['payload']['metadata']['signature']
            signature = decode_data(data=raw_signature)

            id = signature.get('id')
            txn_id = signature.get('txn_id')

            kwargs.update({
                'id': id,
                'txn_id': txn_id
            })
            
        except:
            return response.Response(
                {'detail': 'Invalid signature'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return func(*args, **kwargs)
    return check
