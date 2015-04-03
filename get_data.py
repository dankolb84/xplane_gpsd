#! /usr/bin/python
#This was used to write an nmea.out file in the correct format for testing with gpsd-fake
#to get the correct format required by gpsd, which could then be used for the send_data script
#
#This doesn't really have a use outside of writing nmea files, which are not needed for gpsd
#Dan Kolb <danATdankolbDOTnet> 2015

import socket
import struct
import time
import datetime

WRITE_FILE = "/home/dan/Projects/xplane_data/nmea.out"
params_dict = {}

def write_out():
	global params_dict
	global WRITE_FILE
	cur_time_struct = time.gmtime()
	str_time = "%i%i%i" %(cur_time_struct[3], cur_time_struct[4], cur_time_struct[5])
	params_dict["time"] = str_time
	str_date = "%i%i%i" %(cur_time_struct[0], cur_time_struct[1], cur_time_struct[2])
	params_dict["date"] = str_date
	with open(WRITE_FILE, 'a') as f:
		f.write(write_gpgga(params_dict["lat"],
							params_dict["lon"],
							params_dict["alt_msl"],
							params_dict["time"],
							params_dict["alt_msl"]) + "\n")
		f.write(write_gprmc(params_dict["lat"],
							params_dict["lon"],
							params_dict["alt_msl"],
							params_dict["time"],
							params_dict["date"],
							params_dict["alt_msl"],
							params_dict["ktas"],
							params_dict["mag_head"],
							params_dict["mag_var"]) + "\n")
		f.write(write_gpgsa() + "\n")

def gpsd_out(da_sock):
	global params_dict
	time_zulu = datetime.datetime.utcnow().isoformat() + "Z"
	thing = '{"class":"TPV","tag":"RMC"'\
			+ ',"device":"/dev/pts/6","mode":3,'\
			+ '"time":"' + time_zulu + '","ept"'\
			+ ':0.000,"lat":' + str(params_dict["lat"]) + ',"lon"'\
			+ ':' + params_dict["lon"] + ',"alt":' + params_dict["alt_msl"]\
			+ ',"epv":0.000,'\
			+ '"track":' + params_dict["mag_head"] + ',"speed":'\
			+ params_dict["ktas"] + ',"climb":0.000}'\
			+ "\n"

	da_sock.sendall(thing)

def get_results(struct_data):
	#results = {}
	#
	#lat = struct_data[9:13]
	#print lat
	#lon = struct_data[13:17]

	#print struct.pack('4b', *lat)
	#results["lat"] = struct.unpack('<f', struct.pack('4b', *lat))[0]
	#results["lon"] = struct.unpack('<f', struct.pack('4b', *lon))[0]
	#print results

	results = []
	beg_index = 5
	#results.append(struct_data[5])
	#print "*******"
	#print struct_data
	#print "*******"
	while beg_index < len(struct_data):
		raw_bytes = struct_data[beg_index:beg_index+4]
		results.append(raw_bytes)
		#print tmp_data, beg_index
		#results.append(struct.unpack('<f', struct.pack('4b', *tmp_data))[0])
		beg_index += 4
	
	beg_index = 0
	while beg_index < len(results):
		#iterate through information given in the packet
		#this is 9len byte arrays of 4 items each
		#print "beg", beg_index
		chopped_byte_list = results[beg_index:beg_index + 9]
		#print "chopped: \n", chopped_byte_list
		#print "---"
		#print chopped_byte_list
		record_results(chopped_byte_list)
		beg_index += 9

def convert_to_float(byte_set):
	tmp_data = byte_set
	return float(struct.unpack('<f', struct.pack(str(len(tmp_data)) + "b", *tmp_data))[0])

def record_results(data_list):
	global params_dict
	data_type = data_list[0][0]

	if data_type == 3:
		params_dict["ktas"] = str("%3.2f" % float(convert_to_float(data_list[3])))
	elif data_type == 19:
		params_dict["mag_head"] = str("%3.2f" % float(convert_to_float(data_list[1])))
		params_dict["mag_var"] = str("%3.2f" % float(convert_to_float(data_list[2])))
	elif data_type == 20:
		params_dict["lat"] = str(convert_to_float(data_list[1]))
		params_dict["lon"] = str(convert_to_float(data_list[2]))
		params_dict["alt_msl"] = str(convert_to_float(data_list[3]))
		params_dict["alt_agl"] = str("%8.2s" % convert_to_float(data_list[4]))
		params_dict["lat_north"] = str("%3.7s" % convert_to_float(data_list[5]))
		params_dict["lon_west"] = str("%3.7f" % convert_to_float(data_list[6]))
		#record_results(data_list)

def write_gpgga(lat, lon, alt, da_time, msl):
	'''
	$GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
	1    = UTC of Position
	2    = Latitude
	3    = N or S
	4    = Longitude
	5    = E or W
	6    = GPS quality indicator (0=invalid; 1=GPS fix; 2=Diff. GPS fix)
	7    = Number of satellites in use [not those in view]
	8    = Horizontal dilution of position
	9    = Antenna altitude above/below mean sea level (geoid)
	10   = Meters  (Antenna height unit)
	11   = Geoidal separation (Diff. between WGS-84 earth ellipsoid and
	       mean sea level.  -=geoid is below WGS-84 ellipsoid)
	12   = Meters  (Units of geoidal separation)
	13   = Age in seconds since last update from diff. reference station
	14   = Diff. reference station ID#
	15   = Checksum
	'''
	sen_list = []
	sen_str = ""
	sen_list.append("$GPGGA")
	sen_list.append(da_time)
	sen_list.append(str("%3.8f" %(float(lat))))
	sen_list.append("N")
	sen_list.append(str("%3.8f" %(float(lat))))
	sen_list.append("W")
	sen_list.append("1")
	sen_list.append("3")
	sen_list.append("1.5")
	sen_list.append(str(float(msl) * 0.3048))
	sen_list.append("M")
	sen_list.append("-32")
	sen_list.append("M")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("A")
	for i in sen_list:
		sen_str += i + ","
	sen_out = sen_str[:-1]
	return sen_out	
	print sen_out	

def write_gprmc(lat, lon, alt, da_time, da_date, msl, ktas, course, variation):
	'''
	eg3. $GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*70
              1    2    3    4    5     6    7    8      9     10  11 12


      1   220516     Time Stamp
      2   A          validity - A-ok, V-invalid
      3   5133.82    current Latitude
      4   N          North/South
      5   00042.24   current Longitude
      6   W          East/West
      7   173.8      Speed in knots
      8   231.8      True course
      9   130694     Date Stamp
      10  004.2      Variation
      11  W          East/West
      12  *70        checksum

	'''
	sen_list = []
	sen_str = ""
	sen_list.append("$GPRMC")
	sen_list.append(da_time)
	sen_list.append("A")
	sen_list.append(str("%3.8f" %(float(lat))))
	sen_list.append("N")
	sen_list.append(str("%3.8f" % (float(lat))))
	sen_list.append("W")
	sen_list.append(str(ktas))
	sen_list.append(str(course))
	sen_list.append(str(da_date))
	sen_list.append(str(variation))
	sen_list.append("W")
	sen_list.append("A")

	for i in sen_list:
		sen_str += i + ","
	sen_out = sen_str[:-1]
	return sen_out

def write_gpgsa():
	'''
	GPS DOP and active satellites

	eg1. $GPGSA,A,3,,,,,,16,18,,22,24,,,3.6,2.1,2.2*3C
	eg2. $GPGSA,A,3,19,28,14,18,27,22,31,39,,,,,1.7,1.0,1.3*35


	1    = Mode:
	       M=Manual, forced to operate in 2D or 3D
	       A=Automatic, 3D/2D
	2    = Mode:
	       1=Fix not available
	       2=2D
	       3=3D
	3-14 = IDs of SVs used in position fix (null for unused fields)
	15   = PDOP
	16   = HDOP
	17   = VDOP
	'''
	sen_list = []
	sen_str = ""
	sen_list.append("$GPGSA")
	sen_list.append("A")
	sen_list.append("1")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("")
	sen_list.append("1")
	sen_list.append("1")
	sen_list.append("1")

	for i in sen_list:
		sen_str += i + ","
	sen_out = sen_str[:-1]
	return sen_out		

def process_data(data_byte_list):
	'''

	'''

	global params_dict

	#unpack the data from the packet
	
	data_bytes = struct.unpack(str(len(data_byte_list)) + "b", data_byte_list)
	
	data_list = get_results(data_bytes)

	#print "------"
	#print data_list
	#print "-------"
	#get the type identifier, first thing in the list
	#if data_list[0] == 19:
	#	params_dict["mag_comp"] = data_list[1]
	#	params_dict["mag_comp_var"] = data_list[2]
	#elif data_list[0] == 20:
	#	#lat/lon info
	#	pass
	#elif data_list[0] == 3:
	#	#speed info
	#	pass
	#else:
	#	#unknown. F'get about it
	#	pass
	#print params_dict
def main():
	global params_dict
	cur_time_struct = time.gmtime()
	#print cur_time_struct
	#exit(1)
	str_time = "%i%i%i" %(cur_time_struct[3], cur_time_struct[4], cur_time_struct[5])
	

	blag = "$GPGLL,4046.421,N,-8891.561,W," + str_time + ",A"

	HOST = "127.0.0.1"
	PORT = 49003


	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((HOST, PORT))

	gpsd_port = 2947
	gpsd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	gpsd_socket.bind((HOST, gpsd_port))
	gpsd_socket.listen(1)
	conn, other_guy = gpsd_socket.accept()

	struct_data = ()
	tmp_data = None
	runs = 0
	while 1:

		data, addr = s.recvfrom(1024)
		#print len(data)
		#print struct.unpack("lccccccccccccccccccccccccccccccccc", data)
		#print struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", data)
		#struct.unpack("cccc" + bob + "ifffffffb", data)
		#tmp_data = data
		#print data
		process_data(data)
		#print "processing"
		gpsd_out(conn)
		time.sleep(.2)
		#if runs >= 100:
		#	break
		#runs += 1
		#other_data = struct.unpack("ccccccccccccccccccccccccccccccccccccccccc", data)
		#break
	s.close()

	#print params_dict
	#formats = ["x", "c", "b","B", "?", "h", "H", "i", "l", "L", "q", "Q", "f", "d", "s","p","P"]
	#for i in formats:
	#	try:

	#x = ['Y', '\xdb', '!', 'B']
	#print struct.unpack('<f', struct.pack('4b', *x))
	#bob= struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", tmp_data)

	#bob= struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", tmp_data)
	#print "bob: ", bob
	#print "bob2: ", struct.pack('>b', *bob)
	#print struct.unpack("bbbbb" + "bbbb" + "d" + "bbbbbbbbbbbbbbbbb", tmp_data)
	#get_results(struct.unpack("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", tmp_data))
	#	except:
	#		pass


	#x = [19, 0, 0, 0]
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


blag = "$GPGLL,4046.421,N,-8891.561,W,"



'''
_Vind,_kias |   _Vind,_keas |   Vtrue,_ktas |   Vtrue,_ktgs |   _Vind,__mph |   Vtrue,mphas |   Vtrue,mphgs |   __lat,__deg |   __lon,__deg |   __alt,ftmsl |   __alt,ftagl |   ___on,runwy |   __alt,__ind |   __lat,south |   __lon,_west | 
     65.73390 |       0.00000 |       0.00000 |       0.00000 |      75.64523 |       0.00000 |       0.00000 |      40.47763 |     -88.91023 |     867.13367 |      -0.00000 |       1.00000 |     871.74200 |      39.00000 |     -90.00000 | 
      2.10538 |      10.12598 |      10.25562 |       0.01943 |       2.42283 |      11.80195 |       0.78141 |      40.47763 |     -88.91023 |     867.25488 |       0.12122 |       1.00000 |     867.19513 |      39.00000 |     -90.00000 | 
      4.11687 |      10.36090 |      10.49357 |       0.01934 |       4.73761 |      12.07578 |       0.21820 |      40.47763 |     -88.91023 |     867.33429 |       0.20066 |       1.00000 |     867.31793 |      39.00000 |     -90.00000
  __mag,_comp |   mavar,__deg | 
     18.45793 |       1.13720 | 

'''
