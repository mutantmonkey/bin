#!/usr/bin/python2
################################################################################
# weechat_notify.py - client end of RabbitMQ AMQP weechat notifications
# designed for use with:
# http://www.weechat.org/scripts/source/amqp_notify.rb.html/
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import os.path
import pika
import yaml
from gi.repository import Notify


Notify.init("weechat")

config = yaml.safe_load(open(os.path.expanduser('~/.config/weechat/config.yml')))
connection = pika.BlockingConnection(pika.connection.URLParameters(
    config['rabbitmq']['uri']))
channel = connection.channel()

channel.exchange_declare(exchange=config['rabbitmq']['exchange'], type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=config['rabbitmq']['exchange'], queue=queue_name)

def handle_notify(ch, method, properties, body):
    body = body.replace('!binary', '!!binary')
    data = yaml.safe_load(body)
    n = Notify.Notification.new(
            "{server}.{channel}".format(server=data[':server'],
                channel=data[':channel']),
            data[':message'], 'dialog-information')
    n.show()

channel.basic_consume(handle_notify, queue=queue_name, no_ack=True)
channel.start_consuming()
