import websocket, json
import os
import configparser

# Spark login configurations
config = configparser.ConfigParser()
CONFIG_FILE = os.path.abspath(
    os.path.join(
        __file__,
        os.pardir,
        os.pardir,
        os.pardir,
        "config",
        "postgres.ini",
    )
)
config.read(CONFIG_FILE)

def on_open(ws):
    print("opened")
    auth_data = {
              "type": "hello",
              "apikey": config["COINAPI WEBSOCKET"]["api_key"],
              "heartbeat": False,
              "subscribe_data_type": ["book50"],
              "subscribe_filter_asset_id": ["BTC/USD"]
            }

    ws.send(json.dumps(auth_data))

def on_message(ws, message):
    print(message)

ws = websocket.WebSocketApp(config["COINAPI WEBSOCKET"]["socket"] + "/?type=quote", on_open=on_open, on_message=on_message)
ws.run_forever()