from utils.brokers.rabbitmq import (
    Consumer,
)

consumer = Consumer(broker_url='amqp://localhost')

queue_name = 'service-01'
consumer.declare_queue(queue_name=queue_name)

def callback(ch, method, properties, body):
    print('Received message\n')
    print(f'{body}')
    consumer.ack(method)

print('Started consuming...')

consumer.recieve_messages(queue_name, callback)

consumer.start_consuming()
