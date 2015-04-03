#! /usr/bin/python

#used to test sending data in gpsd format. It worked.
import socket
import struct
import random
import time
import datetime
def get_crap(lat):
	time_zulu = datetime.datetime.utcnow().isoformat() + "Z"
	thing = '{"class":"TPV","tag":"RMC","device":"/dev/pts/6","mode":3,"time":"' + time_zulu + '","ept":0.005,"lat":' + str(lat) + ',"lon":-80.773666667,"alt":258.334,"epv":0.000,"track":19.0300,"speed":0.000,"climb":0.000}' + "\n"
	return thing


def main():
	
	HOST = "127.0.0.1"
	PORT = 2947 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(1)
	#s.connect((HOST,PORT))
	conn,addr= s.accept()
	print conn.recv(1024)
	lat = 40.773666667 
	while 1:
		
		#print get_crap()
		conn.sendall(get_crap(lat))
		lat += .1
		print "sent"
		time.sleep(.1)
		
	s.close()


if __name__ == "__main__":
	main()
