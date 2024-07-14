import json
import time
import uuid
from datetime import UTC, datetime

from pykafka import KafkaClient

# Read coordinates from geojson
input_file = open("./data/bus2.json")
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['testBusData']
producer = topic.get_sync_producer()

data = {}
data['busline'] = "00002"


def generate_checkpoints(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(uuid.uuid4())
        data['timestamp'] = str(datetime.now(UTC))
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        producer.produce(f'{message}'.encode('ascii'))
        time.sleep(1)

        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1


generate_checkpoints(coordinates)


'''


count = 1
while True:
    message = "hello world " + str(count)
    producer.produce(f'{message}'.encode('ascii'))
    print(message)
    count += 1
    if count > 10:
        break
'''
