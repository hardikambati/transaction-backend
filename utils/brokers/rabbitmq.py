# built-in modules
import pika
import json
from typing import Callable


class PikaClient:
    """
    Pika client for publishing and consuming messages through the broker.
    """
    def __init__(self, broker_url: str):
        params = pika.URLParameters(broker_url + "?heartbeat=600")
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()


class Producer(PikaClient):
    """
    RabbitMQ producer
    """
    def declare_queue(self, queue_name):
        """
        Declare a new queue
        """
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, exchange: str,
                        queue_name: str,
                        body: str, **extra):
        """
        Publish message to the queue.
        """
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=body.encode('utf-8'),
            **extra
        )
        print("Message Published to queue:", queue_name)
    
    def close(self):
        """
        Close the connection
        """
        self.channel.close()
        self.connection.close()


class Consumer(PikaClient):
    """
    RabbitMQ consumer
    """
    def declare_queue(self, queue_name, **extra):
        """
        Declare a new queue
        """
        self.channel.queue_declare(queue=queue_name, **extra)

    def recieve_messages(self, queue_name: str, callback: Callable):
        """
        Recieves messages from the queue
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue_name, on_message_callback=callback)
    
    def start_consuming(self):
        """
        Start consuming messages
        """
        self.channel.start_consuming()
    
    def basic_get(self, queue_name):
        """
        Get a single message from queue
        """
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
        body = json.loads(body) if body else {}
        return method_frame, header_frame, body

    def ack(self, method_frame):
        """
        Acknowledge message
        """
        return self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def close(self):
        """
        Close the connection
        """
        self.channel.close()
        self.connection.close()