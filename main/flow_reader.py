#!/usr/bin/env

import subprocess
import re 		 # regex module. Using it to grab digits from file names

class FlowReader:
	""" 
	This class is used to collect flow data from a flow
	sensor using i2c commuication on a Raspberry Pi 
	running Debian. It assumes that you have set up 
	i2c communication. 

	A tutorial to setup i2c communication can be found here:
	https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c


	The subprocess module is used to read the data using the
	'i2cdetect' and 'i2cget' commands

	This class is compatible with both python 2 and python 3
	"""

	def __init__(self,):
		self.data_file = None
		self.i2c_bus = '0x49'
		self.values = []


	# def configure(self):
	# 	"""
	# 	Open a file to record data from and get the i2c_bus.
	# 	"""
	# 	try:
	# 		p = subprocess.Popen('sudo i2cdetect -y 1', stdout=subprocess.PIPE)
	# 		i2c_bus = p.communicate()[0]	# was 0x49 last time
	# 	except OSError as e:
	# 		pass
	# 		#print ("Can't get the i2c bus {}".format(e))
	# 	else:
	# 		self.i2c_bus = i2c_bus


	def create_data_file(self):
		"""
		Creates a new file for the flow data to be stored.
		It does not overwrite any files in the current 
		directory with the word 'flowdata' in the title.
		It also echos the current date and time as the first
		line of the file. 

		Note: It leaves the file open for performance reasons

		...Might consider calling this in the constructor.
		"""

		# list all the file in the current directory
		ls = subprocess.Popen('ls', stdout = subprocess.PIPE)

		# grab the files labeled flowdata
		grep = subprocess.Popen(('grep', 'flowdata'), stdin = ls.stdout, stdout = subprocess.PIPE)

		ls.wait()

		# grab the output of grep 
		flow_files = str(grep.communicate()[0])
		
		# find all the flow data files with numbers	
		file_nums = re.findall(r'(\d+)', flow_files)

		# make the new file name
		if len(file_nums) == 0:
			new_file_name = 'flowdata_1.csv'

		elif len(file_nums) >= 1:
			file_nums = [int(num) for num in file_nums]

			new_num = max(file_nums) + 1
			new_file_name = 'flowdata_{}.csv'.format(new_num)
			
		# write a new file and echo the date
		f = open(new_file_name, 'w')

		# grab the date
		date = subprocess.check_output(['date'])
		date = str(date)
		f.write(date)

		# Leaving the file open for performance reasons.
		f.close()

		# modify the attribute
		self.data_file = f


	def read_sensor(self):
		"""read from the flow sensor. convert hex values to flow values and append the 
		converted value to a data file
		"""
		try:
			# get the flow as a hex value
			command = 'sudo i2cget -y 1 {}'.format(self.i2c_bus)
			p = subprocess.Popen(command, stdout=subprocess.PIPE)

			# get the output from the process and convert from 
			# byte code to a string
			hex_value = str(p.communicate()[0])
		except OSError as e:
			#print ("Cant't read sensor: {}".format(e))
			self.values.append(0)
		else:
			flow_value = hex_value # need to add the conversion formula

			self.values.append(flow_value)
			self.data_file.write(flow_value)


# unit testing
if __name__ == '__main__':

	import sys
	print (sys.version)

	fr = FlowReader()
	fr.create_data_file()

	for i in range(10):
		fr.read_sensor()
		print (fr.values)

	

