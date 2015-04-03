#! /usr/bin/python

#used to test sending information to X-Plane. Doesn't really serve a purpose at this time
import socket
import struct
import random
import time

def get_results(struct_data):
	results = {}
	lat = struct_data[9:13]
	print lat
	lon = struct_data[13:17]
	#convert byte list to float
	results["lat"] = struct.unpack('<f', struct.pack('4b', *lat))[0]
	results["lon"] = struct.unpack('<f', struct.pack('4b', *lon))[0]
	print results


def update_throttle(throt_set):
	''' returns struct to send '''
	#create a buffer to be appended to make our 41 byte message
	
	print "throttle: ", throt_set
	#create beginning of struct
	struct_data = [68, 65, 84, 65, 64, 25, 0, 0, 0,
					0, 0, 0, 0,
					0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	
	#convert float to byte array
	throt_float = throt_set
	packed = struct.unpack('bbbb', struct.pack('f', throt_float))
	#print packed

	i = 0
	for j in range(9, 13):
		struct_data[j] = packed[i]
		i += 1
	
	#print struct_data
	#add our bytes from the float
	#for i in list(struct.unpack('4b', packed)):
	#	struct_data.append(i)
	



	#da_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	#append the buffer
	#for i in da_buffer:
	#	struct_data.append(i)
	
	#convert the message to all bytes
	return struct.pack('41b', *struct_data)

def main():
	




	HOST = "127.0.0.1"
	PORT = 49000

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	struct_data = [ 68, 65, 84, 65, 64, 25, 0, 0, 0, -22, -22, -22, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
	#struct_send =struct.pack('<b', *struct_data)
	#print len(str(struct_data))
	#print PyObject.PyByteArray_FromStringAndSize(struct_data, len(str(struct_data)))
	#print struct.unpack('<b', *struct_data)
	
	
	
	throt_data = [15, -35, -87, 62]
	

	formats = ["x", "c", "b","B", "?", "h", "H", "i", "l", "L", "q", "Q", "f", "d", "s","p","P"]

	#convert float to byte array
	'''
	throt_float = 0.331764668226
	packed = struct.pack('f', throt_float)
	
	print list(struct.unpack('4b', packed))
	



	print struct_data
	

	#send that shiz
	'''
	for x in range(1, 10):
		message = update_throttle(random.random())
		s.sendto(message, (HOST,PORT))
		time.sleep(4)


	#print struct.pack('41b', *struct_data)
	#print struct_data

	#need to convert float to byte list



	s.close()
	#print struct.unpack('<c', *struct_data)
	exit(1)
	tmp_data = None
	while 1:
		data, addr = s.recvfrom(1024)
		print len(data)
		#print struct.unpack("lccccccccccccccccccccccccccccccccc", data)
		#print struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", data)
		#struct.unpack("cccc" + bob + "ifffffffb", data)
		tmp_data = data
		#other_data = struct.unpack("ccccccccccccccccccccccccccccccccccccccccc", data)
		break
	s.close()

	
	#for i in formats:
	#	try:

	#x = ['Y', '\xdb', '!', 'B']
	#print struct.unpack('<f', struct.pack('4b', *x))



	#print struct.unpack("bbbbb" + "bbbb" + "d" + "bbbbbbbbbbbbbbbbb", tmp_data)
	get_results(struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", tmp_data))
	#	except:
	#		pass


	#x = [89, -37, 33, 66]
	#print struct.unpack('<f', struct.pack('4b', *x))

	#x = [-7,-44,-79,-62]
	#print struct.unpack('<f', struct.pack('4b', *x))
	#get_results(tmp_data)

	exit(1)
	#print other_data

	#while data:
	#	print data
	#	data = s.recv(1024)
	#s.close()

if __name__ == "__main__":
	main()

'''
     40.46421 |     -88.91596 |     847.54816 |       0.22889 |       1.00000 |     847.54712 |      39.00000 |     -90.00000 | 

'''
