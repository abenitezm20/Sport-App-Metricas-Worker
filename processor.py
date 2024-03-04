import asyncio
import random
import json
import time
from sqs_service_provider import SqsClientListener
from notificator import Notificator

async def process(data, receiptHandler):
    data = json.loads(data)
    SqsClientListener.delete(receiptHandler)
    check_data(data)
    sleeper = 0.1 * random.randint(1,10)
    print('sleep: ', sleeper)
    await asyncio.sleep(sleeper)
    print('tiempo desde publicación hasta después del sleep', time.perf_counter() - data.get('t1'))

def check_data(data):
    exercise_id = data.get('exercise_id')
    evaluate_heartbeat(data)
    print(exercise_id)

def evaluate_heartbeat(data):
    heartBeat = data.get('current_heartbeat')
    if heartBeat > 140:
        Notificator.user_notification('heartbeat-high')