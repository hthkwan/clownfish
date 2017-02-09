import sys
import socketserver
import socket, threading

hostname = ""
logOptions = ""
srcPort = -1
destPort = -1

class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		#connect to server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect(("hostname", destPort))
		except:
			print("could not connect to %s" % hostname)
			sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) == 4:
		srcPort = int(sys.argv[1])
		hostname = sys.argv[2]
		destPort = sys.argv[3]
	elif len(sys.argv) == 5:
		logOptions = sys.argv[1]
		srcPort = int(sys.argv[2])
		hostname = sys.argv[3]
		destPort = sys.argv[4]
			
	else:
		print ("wrong number of arguments")
		sys.exit(0)
		
		
	server = socketserver.ThreadingTCPServer(("localhost", srcPort), MyTCPHandler)
	server.handle_request()
	
			

