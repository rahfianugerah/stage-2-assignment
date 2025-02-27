import network
import time
import requests
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

TOKEN = "<Token>"  
DEVICE_LABEL = "<Label>"
VARIABLE_LABEL_1 = "temperature"  
VARIABLE_LABEL_2 = "humidity" 

client = MQTTClient(
    "<Client>", 
    "industrial.api.ubidots.com",
    port=1883,
    user="<User>",
    password=""
)

sensor = dht.DHT11(Pin(19))

def publish_payload(payload):
    client.publish('/v1.6/devices/' + DEVICE_LABEL, payload)
    req = requests.post(url='http://127.0.0.1:5000/data', json=payload)

def connect_wifi(): 
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('<Wifi>', '<WifiPassword>')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")

def main():
    connect_wifi()

    print("Connecting to MQTT server... ", end="")
    client.connect()
    print("Connected!")

    prev_payload = "";
    while (True):
        print("Measuring weather conditions... ", end="")
        time.sleep(3)
        sensor.measure() 

        payload = ujson.dumps({
            VARIABLE_LABEL_1: sensor.temperature(),
            VARIABLE_LABEL_2: sensor.humidity()
        })

        if payload != prev_payload:
            print("[INFO] Attemping to send data")
            publish_payload(payload)
            print(payload)
            print("[INFO] finished")
            prev_payload = payload
        else:
            print("No change")


if __name__ == '__main__':
    main()

