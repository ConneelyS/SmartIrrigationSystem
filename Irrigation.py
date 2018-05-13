import paho.mqtt.client as mqtt
import grovepi, time
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

temperature = 5
humidity = 0

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
			
			time.sleep(3)


		moisture_A = analogRead(moisture_sensor_A)
		
		moisturePercentA = int(moisture_A * 0.09775)
		
		if moisture_A > 650:
			digitalWrite(relay_A, 1)
			mqttc.publish("relayA", str(100 - moisturePercentA))
			print str(100 - moisturePercentA)
		else:
			digitalWrite(relay_A, 0)
			mqttc.publish("relayA", str(100 - moisturePercentA))
			print str(100 - moisturePercentA)
			
			time.sleep(0.5)

		moisture_B = analogRead(moisture_sensor_B)

		moisturePercentB = int(moisture_B * 0.09775)
		
		if moisture_B > 650:
			digitalWrite(relay_B, 1)
			mqttc.publish("relayB", str(100 - moisturePercentB))
			print str(100 - moisturePercentB)
		else:
			digitalWrite(relay_B, 0)
			mqttc.publish("relayB", str(100 - moisturePercentB))
			print str(100 - moisturePercentB)
			
			time.sleep(0.5)
		
		moisture_C = analogRead(moisture_sensor_C)
		
		moisturePercentC = int(moisture_C * 0.09775)
		
		if moisture_C < 650:
			digitalWrite(relay_C, 1)
			mqttc.publish("relayC", str(100 - moisturePercentC))
			print str(100 - moisturePercentC)
		else:
			digitalWrite(relay_C, 0)
			mqttc.publish("relayC", str(100 - moisturePercentC))
			print str(100 - moisturePercentC)
			
			time.sleep(0.5)
		
		[temp, hum] = dht(temperature, humidity)
			
		mqttc.publish("temp", str(temp) + " C")
		mqttc.publish("hum", str(hum) + "%")
		print ("Temperature: %d\n" %(temp))
		print ("Humidity: %d\n" %(hum))
		
		time.sleep(2)

publisher()
