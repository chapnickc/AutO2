# test
import socket

def send_data(data_file, connection):
	"""
	Try to open the data file and send it to the client,
	if not, print an error to the screen
	"""
	try:
		f = open(data_file, 'r')
	except IOError as e:
		print ('Received an error of: {}'.format(e))
	else:
		raw_data = f.readlines()
		for line in raw_data:
			connection.send(bytes(line, 'UTF-8'))
		f.close()

	print ('File Sent!')

def main():
	"""
	Accept connections from clients and send them
	the test file.
	"""
	host = ''
	port = 50000
	s = socket.socket()
	s.bind((host, port))

	while True:
		s.listen(5)
		conn, addr = s.accept()
		print ('Connected to: {}'.format(addr))
		data_file = './testdata.txt'
		send_data(data_file, conn)

if __name__ == '__main__':
	main()

