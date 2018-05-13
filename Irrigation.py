#Imports
import paho.mqtt.client as mqtt
import grovepi, time
from grovepi import *

#Establishing a connection to my CloudMqtt account
mqttc = mqtt.Client("ClientA", clean_session = False)
mqttc.username_pw_set("zbrxmtts", "M00ooDe6xxGQ")
mqttc.connect("m21.cloudmqtt.com", "11359", 60)

#Assigning specific sensors to a port number
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

		#Here I am creating a new variable called distant which is being 
		#set to a value from the ultrasonic sensor measurement
		
		distant = ultrasonicRead(ultrasonic_ranger)
		
		#In order to display percentages correctly on the 
		#application we do some basic calculations
		
		distantPercentage = int(distant * 3.125)
		
		#The IF statement uses the new variable to check for high and
		#low values to display a reading of how much water is left within
		#the users water storage tank
		
		if distantPercentage > 95:
			mqttc.publish("irrigation", str("Tank Is Empty"))	#This line of code is the first use of the .publish method that transfers data to CloudMqtt
			print "Tank Is Empty"
		elif distantPercentage < 5:
			mqttc.publish("irrigation", str("Tank Is Full"))
			print "Tank Is Full"
		else:
			mqttc.publish("irrigation", ("Tank Is At "+str(100 - distantPercentage)+"%"))
			print "Tank Is At "+str(100 - distantPercentage)+"%"
			
			time.sleep(3)

		#Moving onto the moisture sensors now and the code is very similar to
		#the ultrasonic code above, once again we use simple maths to get %

		moisture_A = analogRead(moisture_sensor_A)
		
		moisturePercentA = int(moisture_A * 0.09775)
		
		#This is the main function of the codebase where depnding on the value returned
		#from moisture_A (the first moisture sensor) we can see if the soil samples
		#are in need of water. If they are below 650 the relay will trigger and
		#the water will begin flowing through valve A but the others will stay shut
		
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
		
		#The temperature and humidity sensor code is located here
		#There is no funcationality to do with this code but the 
		#sensors are located in the system in order to show how 
		#different climates might effect soil moisture measurements
		
		[temp, hum] = dht(temperature, humidity)
			
		mqttc.publish("temp", str(temp) + " C")
		mqttc.publish("hum", str(hum) + "%")
		print ("Temperature: %d\n" %(temp))
		print ("Humidity: %d\n" %(hum))
		
		time.sleep(2)

publisher()

#The final piece of code runs the publisher method in order
#to excute the code and retrieve the values required
