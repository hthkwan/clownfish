import sys
import socketserver
import socket, threading

hostname = ""
logOptions = ""
srcPort = -1
destPort = -1

class MyTCPHandler(socketserver.BaseRequestHandler):
	BUFFER_SIZE = 4096
	def handle(self):
		#connect to server
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((hostname, destPort))
		except:
			print("could not connect to %s" % hostname)
			s.close()
			sys.exit(0)
			
		while 1:
			data = self.request.recv(self.BUFFER_SIZE)
			if len(data) == self.BUFFER_SIZE:
				while 1:
					try:  # error means no more data
						data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
					except:
			#if connection is closed, end the program
			break
			if data == '':
				break
			
			#data to be printed and logged
			dataTxt = data.decode("utf-8")
			print("<-- %s" % dataTxt)
			
			s.send(data)
			
			#receive data
			response = s.recv(self.BUFFER_SIZE)
			
			#data to be printed and logged
			responseTxt = response.decode("utf-8")
			
			print("--> %s" % responseTxt)
			
			self.request.sendall(response)
			

if __name__ == "__main__":
	if len(sys.argv) == 4:
		srcPort = int(sys.argv[1])
		hostname = sys.argv[2]
		destPort = int(sys.argv[3])
	elif len(sys.argv) == 5:
		logOptions = sys.argv[1]
		srcPort = int(sys.argv[2])
		hostname = sys.argv[3]
		destPort = int(sys.argv[4])
			
	else:
		print ("wrong number of arguments")
		sys.exit(0)
		
		
	server = socketserver.ThreadingTCPServer(("localhost", srcPort), MyTCPHandler)
	server.handle_request()
	
			

