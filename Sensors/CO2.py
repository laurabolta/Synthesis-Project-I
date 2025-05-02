
import paho.mqtt.client as mqtt
import json

def send_alert(classroom, co2_value):
    print(f"ALERT: CO₂ in {classroom} is {co2_value} ppm — open windows or improve ventilation.")

WATCHED_DEVICES = {
    "q4-1003-7456": "Q4-1003",
    "eui-24e124128c147446": "Q2-1011",
    "eui-24e124128c147470": "Q1-1013"
}

CO2_THRESHOLD = 1000

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload
        string = payload.decode('utf-8')
        data = json.loads(string)
        sensor = data["end_device_ids"]["device_id"]
        
        if sensor not in WATCHED_DEVICES:
            return  # Ignoring other devices like open lab
        
        # Extract CO2 value (adjust if your structure is different)
        co2 = data["uplink_message"]["decoded_payload"].get("co2")

        if co2 is not None:
            room = WATCHED_DEVICES[sensor]
            print(f"[{room}] CO₂ level: {co2} ppm")
            if co2 >= CO2_THRESHOLD:
                send_alert(room, co2)
    except Exception as e:
        print(f"Error processing message: {e}")
    
    #print(sensor)
    #print(data["uplink_message"]["decoded_payload"])

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("sensors-openlab@ttn", password="NNSXS.7OSRB3R5DM6S6O3JSQBPZOOLCULA5KAHNRDN4NA.4GNPE2VGUTZBENDGGZLKD6IUT7JDT4HZDJWFDX24XJMBNH36VA7Q")
client.connect("eu1.cloud.thethings.network", 1883, 60)
client.loop_forever()


