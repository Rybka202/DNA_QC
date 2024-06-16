import sys, traceback

import pika


async def send_message(fileName: str):
    conn_param = pika.ConnectionParameters('rabbitmq', 5672, virtual_host='/', credentials=pika.credentials.PlainCredentials('guest', 'guest'))
    connection = pika.BlockingConnection(conn_param)
    channel = connection.channel()
    channel.exchange_declare(exchange='exchange',
                             exchange_type='direct')

    channel.queue_declare(queue='unprocessed_queue')

    channel.queue_bind(exchange='exchange',
                       queue='unprocessed_queue',
                       routing_key='unprocessed')

    channel.basic_publish(exchange='exchange',
                          routing_key='unprocessed',
                          body=fileName)
    connection.close()