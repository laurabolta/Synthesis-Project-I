
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pandas as pd
import os

# Load and preprocess final_data from CSV
final_data = pd.read_csv('Sensors/merged_occupacio_professors.csv')
final_data['start date'] = final_data['start date'].astype(str).str.strip()
final_data['start time'] = final_data['start time'].astype(str).str.strip()
final_data['end time'] = final_data['end time'].astype(str).str.strip()
final_data['class Id'] = final_data['class Id'].astype(str).str.strip()

def send_alert(classroom, final_data, time_str, date_str, co2_level):
    current_time = datetime.strptime(time_str, "%H:%M")
    current_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    
    # Filter rows for matching date and class ID
    candidates = final_data[final_data['class Id'].str.upper() == classroom.upper()]
    candidates = candidates[candidates['start date'] == date_str]

    # Check if time falls in the scheduled class time
    def is_within(row):
        start = datetime.strptime(row['start time'], "%H:%M")
        end = datetime.strptime(row['end time'], "%H:%M")
        return start <= current_time <= end

    # Apply time filter
    active_classes = candidates[candidates.apply(is_within, axis=1)]

    if not active_classes.empty:
        # Save the info in Alert_Message folder
        alert_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Alert_Message")
        os.makedirs(alert_dir, exist_ok=True)  # Create folder if it doesn't exist
        alert_file_path = os.path.join(alert_dir, "co2_alerts_log.csv")

        for _, row in active_classes.iterrows():
            print(f"ALERT: CO₂ level is {co2_level} ppm in {classroom} during '{row['Assignatura']}'")
            print(f"Notifying professor(s): {row['Id Anònim PD']}")

            alert_entry = {
                "ProfessorID": row['Id Anònim PD'],
                "Classroom": classroom,
                "Date": date_str,
                "AlertTime": time_str,
                "StartTime": row["start time"],
                "EndTime": row["end time"],
                "CO2_ppm": co2_level,
                "Subject": row["Assignatura"]
            }

            # Write or append the alert
            pd.DataFrame([alert_entry]).to_csv(
                alert_file_path,
                mode="a",
                index=False,
                header=not os.path.exists(alert_file_path)
            )
    
    else:
        print(f"No active class found in {classroom} at {time_str} on {date_str}.")



WATCHED_DEVICES = {
    "q4-1003-7456": "Q4/1003",
    "eui-24e124128c147446": "Q2/1011",
    "eui-24e124128c147470": "Q1/1013"
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
                print(f"ALERT: CO₂ in {room} is {co2} ppm — open windows or improve ventilation.")
                now = datetime.now()
                date_str = now.strftime("%d/%m/%Y")
                time_str = now.strftime("%H:%M")
                
                send_alert(room, final_data, time_str, date_str, co2)
                
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


