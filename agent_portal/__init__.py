from gevent import monkey, spawn
async_mode = 'gevent'
monkey.patch_all()
# import eventlet
# async_mode = 'eventlet'
# eventlet.monkey_patch()

import os
import json
import time
from threading import Thread
from bson import json_util
from flask import Flask, session, render_template, make_response, \
  request, redirect, g, current_app, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, \
  close_room, rooms, disconnect
import pika 

# from async_consumer import AsyncMqConsumer
# example = AsyncMqConsumer('amqp://guest:guest@localhost:5672/%2F')
# example.run()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    
app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY'] = 'dsflskdf10370322$@#$'

socketio = SocketIO(app, async_mode=async_mode)
thread = None

NAMESPACE = None
# NAMESPACE = '/skadoosh_agent_portal'

def callback(ch, method, properties, body):
  content = json.loads(body.decode('utf-8'))
  print(" [x] Received %r" % content)
  ch.basic_ack(delivery_tag = method.delivery_tag)
  try:
    socketio.emit('general_response',{
      'data': json.dumps(content),
      'count': 0
    })
    print("Emitting to websocket")
  except Exception as e:
    print(e)
    
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
resonse_channel = connection.channel()
resonse_channel.basic_qos(prefetch_count=1)
resonse_channel.queue_declare(queue='agent_response_queue', durable=True)

def consumer():
  global connection
  channel = connection.channel()
  channel.queue_declare(queue='task_queue', durable=True)
  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(callback, queue='task_queue')
  channel.start_consuming()

spawn(consumer)

@app.route("/")
def home():
  return render_template('home.jinja2')

@app.route('/api/ask_agent')
def ask_agent():
  data = request.args.get('query', 'No question asked by the user')
  count = session['receive_count'] = session.get('receive_count', 0) + 1
  socketio.emit('general_response',
                  {'data': data, 'count': count})
  return make_response("",200)

@socketio.on('agent_answer', namespace=NAMESPACE)
def test_message(message):
    global resonse_channel
    resonse_channel.basic_publish(exchange='',
                      routing_key='agent_response_queue',
                      body=message['data'],
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print("*** Sending message '%s' to agent_response_queue" % message['data'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('general_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('join', namespace=NAMESPACE)
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('general_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('leave', namespace=NAMESPACE)
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('general_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('close room', namespace=NAMESPACE)
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('general_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])

@socketio.on('disconnect request', namespace=NAMESPACE)
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('general_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    emit('general_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected', request.sid)
    