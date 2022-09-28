#!/usr/bin/env python
"""
Получение сообщений

"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

channel.basic_consume(callback,
                      queue='hello',
                      auto_ack=True)

channel.start_consuming()