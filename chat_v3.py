'''IMPORTANT INSTRUCTIONS IN A COMMENT AT THE BOTTOM'''
from socket import *
import sys
import argparse
import random
import threading

#Create the arguments to be inputted when running program
parser = argparse.ArgumentParser(description = 'Simple python chat app v_3')
parser.add_argument('other_host_ip', type = str, metavar = '', help = 'Other host\'s IP') #Other host's IP

args = parser.parse_args()

serverIP = args.other_host_ip #IP of other host
recievePort = random.randint(21000,22000) #Local host's port, picked randomly from range 21000 to 22000, there is a chance that both hosts can match, launch again for differnet numbers
print('Local port is: ', recievePort)
on_port = [] #Other host's port. intianlized as a list as i was having trouble with threads and assignment
lock = threading.Lock() #Create thread lock
found = False #This is used if the user is designated as User1 as after findind User2's port, there is no need to look again
threads = [] #list of threads
#Function to scan ports using threads
def portscan(port):
    s = socket(AF_INET, SOCK_STREAM) #Create socket
    s.settimeout(0.5) #Set timeout to 0.5 seconds
    #Try to connect using given IP and port passed into function
    try:
        con = s.connect((serverIP, port))
        lock.acquire() #If connection is succssesful lock threads
        on_port.append(port) #Append port number to list, since only one port will be availble we can use index 0 to call it when needed
        con.close() #Close connection
        lock.release() #Release lock
    except:
        pass
#Here we initialize the list of threads and give each thread the parameter to be passed to portscan method
for x in range(21000,22001): #range is to 22001 because second index is exclusive and we want 22000 to be in range
    t = threading.Thread(target = portscan, kwargs = {'port':x})
    threads.append(t)
#Start all thraeds
for k in threads:
    k.start()
#Wait for all threads to finish before continuing
for j in threads:
     j.join()
#If other host's port was found then print it, otherwise continue with code
if(on_port):
    print('Other host\'s port is: ', on_port[0])
#Create TCP sockets
sendSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket.bind(('0.0.0.0', recievePort)) #Bind socket
recieveSocket.listen(1) #Listen for incoming connections
connectionSocket = None #connectionSocket was declared here to make sure program doesn't get stuck on .accept() in while loop using if statement

try:
    #App will try to connect to other host if they are on
    sendSocket.connect((serverIP, on_port[0]))
    sender = 'From User1: ' #This signifies that this is User2 and the sender is User1
    print('Client found, waiting for message')
except:
    #If app couldn't connect to other host it will be designated as User1run this code
    sender = 'From User2: ' #This signifies that this is User1 and the sender is User2
    print('Cannot find client to connect to, \"Enter your message:\" will appear once client is found')
while True:
    #If statment here to make sure that we don't get stuck in .accept() after accepting the connection the first time
    if(connectionSocket == None):
        connectionSocket, addr = recieveSocket.accept() #Here we accept the first connection which is the one that test ports
        connectionSocket, addr = recieveSocket.accept() #Here we accept the connection of the actual host
    #This part of the code will be run if the user is designated as User2
    if(sender == 'From User1: '):
        sentence  = connectionSocket.recv(1024).decode() #Recieve sentence from User1 and if sentence is "exit" then close socket and exit app, otherwise print sentence
        if(sentence == 'exit'):
            print('Other user issued exit')
            print('Terminating...')
            connectionSocket.close()
            sys.exit()
        print(sender)
        print(sentence)
        word = input('Enter your message: ') #Send message to User1 if word is "exit" then close socket and exit app, otherwise send word
        if(word == 'exit'):
            print('Exit issued')
            print('Terminating...')
            sendSocket.send(word.encode())
            connectionSocket.close()
            sys.exit()
        sendSocket.send(word.encode())
    #This part of the code will be run if the user is designated as User1
    if(sender == 'From User2: '):
        threads2 = []
        word = input('Enter your message: ') #User1 sends first
        #Since at the beginning User1 won't be connected to User2, it will try to connect to it here
        if(found == False): #If User1 hasn't found User2's port, look for it here
            for x in range(21000,22001):
                t = threading.Thread(target = portscan,kwargs = {'port':x})
                threads2.append(t)
            #Start all thraeds
            for k in threads2:
                    k.start()
            # Wait for all threads to finish before continuing
            for j in threads2:
                    j.join()
        try:
            sendSocket.connect((serverIP, on_port[0]))
            print('Other host\'s port is: ', on_port[0]) #Print other host's port
            found = True #We set found to true because the other host's port was found
        except:
            exception = 'exception happened'
        sendSocket.send(word.encode()) #Send the word to User2, if word sent is "exit" then close connection and exit app, otherwise continue the code
        if(word == 'exit'):
            print('Exit issued')
            print('Terminating...')
            connectionSocket.close()
            sys.exit()
        sentence  = connectionSocket.recv(1024).decode() #If sentence recieved from User2 is "exit" then close connection and exit app, otherwise print sentence
        if(sentence == 'exit'):
            print('Other user issued exit')
            print('Terminating...')
            connectionSocket.close()
            sys.exit()
        print(sender)
        print(sentence)



'''
INSTRUCTIONS
The app takes other host's IP address as argument before running the app

IMPORTANT
Launch one app first and wait until 'Cannot find client to connect to, "Enter your message:" will appear once client is found' prints, it may take a moment
If you don't wait until it prints then the apps will not run as intended
after 'Cannot find client to connect to, "Enter your message:" will appear once client is found' is printed you can run the second app
then the second app will print 'Client found, waiting for message' and the first app will have "Enter your message: "
after that the apps will work as intended with the first app launched being the one that sends first

To exit, exit message must all be in lower case

In this app we used multithreading to speed up port scanning
'''
