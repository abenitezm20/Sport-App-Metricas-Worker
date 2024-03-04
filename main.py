from sqs_service_provider import SqsClientListener
from processor import process
import asyncio
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/health')
def health():
    return '', 200

def run_worker():
    asyncio.run(main())

async def main():
    while True:
        messages = SqsClientListener.dequeue()
        # messages = [
        #     {
        #         "Body": "hi1",
        #         "ReceiptHandle": 1
        #     },
        #     {
        #         "Body": "hi2",
        #         "ReceiptHandle": 2
        #     },
        #     {
        #         "Body": "hi3",
        #         "ReceiptHandle": 3
        #     },
        #     {
        #         "Body": "hi4",
        #         "ReceiptHandle": 4
        #     },
        #     {
        #         "Body": "hi5",
        #         "ReceiptHandle": 5
        #     }
        # ]
        if not messages:
            # await asyncio.sleep(1)
            continue

        tasks = []
        start = time.perf_counter()
        for message in messages:
            body = message.get('Body')
            receipt = message.get('ReceiptHandle')
            task = asyncio.create_task(process(body, receipt))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start
        print('tiempo empleado en todo: ', elapsed)

if __name__ == "__main__":
    t = Thread(target=run_worker, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=3001)