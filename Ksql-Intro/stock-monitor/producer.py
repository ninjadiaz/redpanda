import json
import websocket
from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers = "localhost:19092",
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

topic = "stock-updates"
    
def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

# Message handlers
def on_ws_message(ws, message):
    # print(message)
    data = json.loads(message)["data"]
    records = [
        {
            "symbol":d["s"],
            "price":d["p"],
            "volume":d["v"],
            "timestamp":datetime.fromtimestamp(d["t"]/1000).strftime("%Y-%m-%d %H:%M:%S")
        }
        for d in data
    ] 
    for record in records:
        print(record)
        future = producer.send(topic,value=record)
        future.add_callback(on_success)
        future.add_errback(on_error)

def on_ws_error(ws, error):
    print(error)

def on_ws_close(ws, close_status_code, close_msg):
    producer.flush()
    producer.close()
    print("### closed ###")

def on_ws_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

# Produce asynchronously with callbacks
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cjfcc21r01qhblojr5s0cjfcc21r01qhblojr5sg",
                              on_message = on_ws_message,
                              on_error = on_ws_error,
                              on_close = on_ws_close)
    ws.on_open = on_ws_open
    ws.run_forever()
