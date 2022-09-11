'''IMPORTANT NOTE AT THE BOTTOM'''
from socket import *

registered_adds = {} #Dictionary that will contain hosts' IP addresses as keys and the hosts' ports as values
trackerPort = 55555 #Tracker port number
trackerRecieveSocket = socket(AF_INET, SOCK_STREAM) #Create tracker recieve socket
trackerRecieveSocket.bind(('0.0.0.0', trackerPort)) #Bind
trackerRecieveSocket.listen(1) #Listen for incoming connections
print('Tracker is ready')

while True:
    connectionSocket, addr = trackerRecieveSocket.accept() #Aceept connection
    hostPort = connectionSocket.recv(1024).decode() #Decode port number sent by host
    registered_adds.update({addr[0] : int(hostPort)}) #Update dictionary with host's IP and port, port was sent as string so it was casted back to int
    print('Registered addresses are:') #Print registered addresses and their corresponding ports
    print(registered_adds)
    response = [] #This list will contain other host's IP and ports if they are already registered, if not it will return empty
    for address in registered_adds.keys():
        if(address != addr[0]):
            response.append(address)
            response.append(registered_adds[address])
    list_to_str = str(response) #Make list as string so we can use .encode()
    connectionSocket.send(list_to_str.encode())
    connectionSocket.close() #Close connection

'''
The whole system (apps and tracker) are implemented in a way such that there can be a max of two apps, adding a third will register on the tracker
but will mess up the apps and they won't work correctly
Tracker needs to be reset to work with 2 new connections as previously registered IPs may mess up connections
'''
