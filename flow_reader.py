import subprocess
import re 		 # regex module. Using it to grab digits from file names

class FlowReader:
	""" 
	This class is used to collect flow data from a flow
	sensor using i2c commuication on a Raspberry Pi 
	running Debian. It assumes that you have set up 
	i2c communication. 

	The subprocess module is used to read the data using the
	'i2cdetect' and 'i2cget' commands

	A tutorial to setup i2c communication can be found here:
	https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
	"""

	def __init__(self,):
		self.data_file = None
		self.i2c_bus = None
		self.values = []

	def configure(self):
		"""
		Open a file to record data from and get the i2c_bus.
		"""
		i2c_bus = subprocess.check_output(['sudo i2cdetect -y 1'], shell = True)
		# was 0x49 last time

		self.i2c_bus = i2c_bus


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
		flow_files = grep.communicate()[0]
		
		# find all the flow data files with numbers	
		file_nums = re.findall(r'(\d+)', flow_files)

		if len(flow_files) is 0:
			new_file_name = 'flowdata.csv'

		elif len(flow_files) >= 1 and len(file_nums) < 1:
			new_file_name = 'flowdata_1.csv'

		elif len(flow_files) >= 1 and len(file_nums) >= 1:
			file_nums = [int(num) for num in file_nums]

			new_num = max(file_nums) + 1
			new_file_name = 'flowdata_{}.csv'.format(new_num)
			print (new_file_name)

		# write a new file and echo the date
		f = open(new_file_name, 'w')

		# grab the date
		date = subprocess.check_output(['date'])
		f.write(date)

		# Leaving the file open for performance reasons.
		#f.close()

		# modify the attribute
		self.data_file = f



	def read_sensor(self):
		"""read from the flow sensor.	convert hex values to flow values and append the 
		converted value to a data file
		"""
		try:
			# get the flow as a hex value
			command = 'sudo i2cget -y 1 {}'.format(self.i2c_bus)
			hex_value = subprocess.check_output([command], shell = True)
		except subprocess.CalledProcessError as e:
			print (e)
			self.values.append(0)
		else:
			flow_value = hex_value # + math
			self.values.append(flow_value)
			self.data_file.write(flow_value)



if __name__ == '__main__':
	fr = FlowReader()
	fr.create_data_file()

	fr.read_sensor()
	

