import RPi.GPIO as GPIO
from DHT11 import DHT11
from LPS331AP import LPS331AP
import time
import datetime

def gpioSetup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.cleanup()
	
def main():
	
	gpioSetup()
	sensor = DHT11(14) #odczyt DHT11 na pinie 14
	sensor_2 = LPS331AP()
	
	while True:
		
		ERR_CODE, temperature, humidity = sensor.getValues()
		pressure = sensor_2.getPressure()
		altitude = sensor_2.getAltitude()
		if ERR_CODE == 0:
			print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
			print("Temperatura: %d *C" % temperature)
			print("Wilgotnosc powietrza: %d %%" % humidity)
			print("Cisnienie powietrza: %.2f mb" % pressure)
			print("Wysokosc: %.2f m" % altitude)
			print("-----------------------------")
		else:
			print(ERR_CODE)
		time.sleep(3)

main()
