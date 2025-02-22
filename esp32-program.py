# Import required library
import network
import time
import requests
import dht
import ujson

from machine import Pin
from umqtt.simple import MQTTClient

# Variables
TOKEN = "<TokenUbidots>"  
DEVICE_LABEL = "<YourDeviceLabel>" 
VARIABLE_LABEL_1 = "temperature"  
VARIABLE_LABEL_2 = "humidity" 

# Client
client = MQTTClient(
    "<UbidotsClient>", 
    "industrial.api.ubidots.com",
    port=1883,
    user="<user-ubidots>",
    password=""
)

# Using DHT11 Sensor
sensor = dht.DHT11(Pin(19))

def publish_payload(payload):
    """
    Send payload to Ubidots via MQTT 
    Send POST to Flask API (http://<IPSERVER>:5000/data).
    """
    # Send data to Ubidots
    client.publish('/v1.6/devices/' + DEVICE_LABEL, payload)

    # Send data to Flask server (Flask server is connected to MongoDB)
    try:
        req = requests.post(url='<YourURL>/data', json=ujson.loads(payload))
        print("[INFO] Status code:", req.status_code)
    except Exception as e:
        print("[ERROR] Failed send to server Flask:", e)

def connect_wifi(): 
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('<Wifi>', '<Password>')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected! IP:", sta_if.ifconfig())

# Main
def main():
    connect_wifi()

    print("Connecting to MQTT server... ", end="")
    client.connect()
    print("Connected!")

    prev_payload = ""
    while True:
        print("Measuring weather conditions... ", end="")
        time.sleep(3)
        sensor.measure() 

        payload_dict = {
            VARIABLE_LABEL_1: sensor.temperature(),
            VARIABLE_LABEL_2: sensor.humidity()
        }
        payload = ujson.dumps(payload_dict)

        if payload != prev_payload:
            print("[INFO] Attempting to send data")
            publish_payload(payload)
            print(payload)
            print("[INFO] Finished sending data")
            prev_payload = payload
        else:
            print("No change")

if __name__ == '__main__':
    main()