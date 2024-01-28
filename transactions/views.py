import json
from rest_framework import (
    views,
    status,
    response,
    permissions,
)

# Swagger Modules
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# custom
from . import (
    models, 
    serializers,
)
from . import (
    serializers,
)
from utils import helpers
from utils.config import (
    RABBITMQ_SERVER_URL,
    SERVICE01_QUEUE_NAME,
)
from utils.swagger import responses
from utils.brokers.rabbitmq import Producer


class TransactionAPIView(views.APIView):

    model_class        = models.Transaction
    serializer_class   = serializers.TransactionSerializer
    permission_classes = [permissions.IsAuthenticated,]

    @swagger_auto_schema(
        responses=responses.GET_RESPONSES,
        manual_parameters=[
            openapi.Parameter(
                name='id', 
                in_='query', 
                type=openapi.TYPE_STRING, 
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        query = self.model_class.objects.all()
        id = request.query_params.get('id')

        if id:
            query = query.filter(id=id)

        serializer = serializers.TransactionSerializer(query, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=responses.POST_RESPONSES,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name"],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        helpers.pop_from_data(
            pop_list=['metadata', 'txn_id', 'status', 'user'],
            data=data
        )

        # popuplate data with logged in user
        data.update({'user': request.user.id})

        serializer = serializers.TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            signature = helpers.encode_data(
                {'id': serializer.data.get('id'), 'txn_id': serializer.data.get('txn_id')}
            )

            payload = {
                'data': serializer.data,
                'metadata': {
                    'signature': signature, 
                },
                'extra_data': {},
            }
            
            # send data to service-01 queue
            queue_name = SERVICE01_QUEUE_NAME
            producer = Producer(broker_url=RABBITMQ_SERVER_URL)
            producer.declare_queue(queue_name=queue_name)
            producer.publish_message(
                exchange='',
                queue_name=queue_name,
                body=json.dumps({
                    'payload': payload
                })
            )

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
