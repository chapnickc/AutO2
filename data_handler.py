
import socket

class DataHandler():
    """
    This class is made to act as a client to read data 
    from a socket and parse it appropriately.
    """
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.host = host
        self.port = port
        self.values = [] # a vector to store the incoming data

    def connect(self):
        """
        Attempt to connect to the server. If no connection 
        is made, the class's socket will be destroyed and 
        a new one will be created. Otherwise, connect to the 
        host and let the user know.
        """
        try:
            self.sock.connect((self.host, self.port))
        except socket.error as e:
            print ('Received and error: {}'.format(e))
            print ('Creating a new socket new socket...')
            self.sock.close()
            self.sock = socket.socket()
            self.sock.connect((self.host, self.port))
        else:
            print ('Connected to ', self.host)

    def disconnect(self):
        """
        Disconnect from the host and display a message
        """
        try:
            self.sock.close()
            print ("Disconnected from ", self.host)
        except socket.error as e:
            print ('Received and error: {}'.format(e))

    def listen(self):
        """
        Listen for incoming data and format it appropriately.
        This assumes that the data is coming in the appropriate 
        format from convert_data.py which is in:
        AutO2/Engineer/Programs/Sample_data as of March 15, 2016.

        The sample data that goes into convert_data.py comes from 
        https://www.physionet.org/. In particular, search for Spo2
        in the database. On March 15 2016, I was able to use this link:
        https://www.physionet.org/search-results.shtml?q=spo2&sa=Search
        """
        # read in 100 bytes from the socket and join the data.
        # Note: the number of bytes is important, and is dependent
        # on the format from which was output  from convert_data.py
        # A value of 100 bytes prevents any partial values from being
        # read in from the socket.
        
        # set a 1.00 second timeout for the recv method
        self.sock.settimeout(0.1) 
        try:
            data = self.sock.recv(100).decode('UTF-8') 
        except socket.timeout as e:
            print (e)
            self.values.append(0)
            return self.values
        else:
            data = ''.join(data)
            data = data.split('\n')

            # append the new values to the object's values attribute
            for element in data:
                if len(element) > 1:
                    self.values.append(float(element))

            return self.values 

# unit test
if __name__ == '__main__':
    host = socket.gethostname()
    port = 50000

    dh = DataHandler(host, port)
    dh.connect()

    a = dh.listen()
    print (a)

