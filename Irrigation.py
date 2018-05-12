import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from grovepi import *

mqttc = mqtt.Client("ClientA", clean_session = False)
mqttc.username_pw_set("zbrxmtts", "M00ooDe6xxGQ")
mqttc.connect("m21.cloudmqtt.com", "11359", 60)

moisture_sensor_A = 0
moisture_sensor_B = 1
moisture_sensor_C = 2

relay_A = 4
relay_B = 3
relay_C = 2

ultrasonic_ranger = 6

def publisher():
	while True:
		
		distant = ultrasonicRead(ultrasonic_ranger)
		
		distantPercentage = int(distant * 3.125)
		
		if distantPercentage > 95:
			mqttc.publish("irrigation", str("Tank Is Empty"))
			print "Tank Is Empty"
		elif distantPercentage < 5:
			mqttc.publish("irrigation", str("Tank Is Full"))
			print "Tank Is Full"
		else:
			mqttc.publish("irrigation", ("Tank Is At "+str(100 - distantPercentage)+"%"))
			print "Tank Is At "+str(100 - distantPercentage)+"%"
			
		time.sleep(5)
		
		moisture_A = analogRead(moisture_sensor_A)
		
		if moisture_A <=650:
			digitalWrite(relay_A, 1)
			mqttc.publish("relayA", str(moisture_A))
		else:
			digitalWrite(relay_A, 0)
			mqttc.publish("relayA", str(moisture_A))
			print moisture_A
			
		moisture_B = analogRead(moisture_sensor_B)
		
		if moisture_B <= 650:
			digitalWrite(relay_B, 1)
			mqttc.publish("relayB", str(moisture_B))
		else:
			digitalWrite(relay_B, 0)
			mqttc.publish("relayB", str(moisture_B))
			print moisture_B
		
		moisture_C = analogRead(moisture_sensor_C)
		
		if moisture_C <= 650:
			digitalWrite(relay_C, 1)
			mqttc.publish("relayC", str(moisture_C))
		else:
			digitalWrite(relay_C, 0)
			mqttc.publish("relayC", str(moisture_C))
			print moisture_C
			
		time.sleep(3)
		
		print "Published"
publisher()
