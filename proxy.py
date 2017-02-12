import sys, socket, threading, time, binascii

hostname = ""
logOptions = ""
destPort = -1
incomeArrow = "<-- "
outgoingArrow = "--> "

def loggingOption(data,arrow):
    if(logOptions=='-raw'):
        dataTxt = data.decode("utf-8")
        dataList = dataTxt.split('\n')
        for d in dataList:
            if(d!=''):
                print("%s %s" %(arrow,d))
        return

    elif(logOptions=='-hex'):
        dataHex = binascii.hexlify(data)
        dataHex = dataHex.decode("utf-8")
        dataTxt = data.decode("utf-8")




        print("%s %s" % (arrow, dataHex))

        return
    else:
        return


class ProxyServer(threading.Thread):
    def __init__(self,srcPort,host='localhost'):
        threading.Thread.__init__(self)
        self.port=srcPort
        self.host=host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socks = []

        try:
            self.server.bind((self.host,self.port))
            self.dest.connect((hostname,destPort))

        except socket.error:
            print("Could not find socket: %s" %socket.error)
            sys.exit()

        self.server.listen(10)

    def shutdownProxy(self):
        self.server.close()

    def runThread(self,sock,address):
        date = time.strftime("%c")
        print("New Connection: %s, from %s"%(date,address[0]))
        BUFFER_SIZE = 4096
        while True:
            data = sock.recv(BUFFER_SIZE)
            dataTxt = data.decode("utf-8")

            ##LOGGING
            loggingOption(data,outgoingArrow)
            ##LOGGING

            if(dataTxt=='shutdown\n'):
                self.socks.remove(sock)
                break

            self.forward(data)
        sock.close()

    def forward(self,data):
        self.dest.sendall(data)


    def listenThread(self):
        BUFFER_SIZE = 4096
        while True:
            data = self.dest.recv(BUFFER_SIZE)
            dataTxt = data.decode("utf-8")

            ##LOGING
            loggingOption(data,incomeArrow)
            ##LOGGING

            for s in self.socks:
                s.sendall(data)


    def run(self):
        print("Port Logger Running srcPort= %d hostname= %s destPort= %d" %(srcPort,hostname,destPort))

        while True:
            sock, address = self.server.accept()

            threading.Thread(target=self.runThread,args=(sock,address)).start()
            self.socks.append(sock)
            threading.Thread(target=self.listenThread).start()

if __name__ == '__main__':
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
        print("wrong number of arguments")
        sys.exit(0)


    server = ProxyServer(srcPort)
    # Run the chat server listening on PORT
    server.run()