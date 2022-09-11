'''IMPORTANT INSTRUCTIONS IN A COMMENT AT THE BOTTOM'''
from socket import *
import sys
import argparse
import random

#Create the arguments to be inputted when running program
parser = argparse.ArgumentParser(description = 'Simple python chat app v_2')
parser.add_argument('tracker_ip', type = str, metavar = '', help = 'Tracker\'s IP') #Tracker's IP
parser.add_argument('tracker_port', type = int, metavar = '', help = 'Tracker\'s port') #Tracker's port

args = parser.parse_args()

trackerIP = args.tracker_ip #IP of tracker
trackerPort = args.tracker_port #Port of tracker
trackerSendSocket = socket(AF_INET, SOCK_STREAM) #Create tracker socket
recievePort = random.randint(21000,22000) #Local host's port, picked randomly from range 21000 to 22000, there is a chance that both hosts can match, launch again for differnet numbers
recieveSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket.bind(('0.0.0.0', recievePort))
try:
    trackerSendSocket.connect((trackerIP, trackerPort)) #connect to tracker, if tracker isn't on, end program, may take a moment (20secs to 1min)
except:
    print("Tracker isn't on, Terminating")
    sys.exit()
trackerSendSocket.send(str(recievePort).encode()) #Send port number to tracker, sent as string to call .encode()
str_list = trackerSendSocket.recv(1024).decode('utf-8') #Recieve list containing other host's IP and port if they are available, empty if not
add_port_list = eval(str_list) #Since tracker sends list as string, we convert it back to list here
trackerSendSocket.close() #Was having trouble with sending info later on for the first host to get info on the second so we close socket and create it again
trackerSendSocket = socket(AF_INET, SOCK_STREAM)

#If list is not empty, assign other host's IP and port
if(add_port_list):
    serverIP = add_port_list[0] #IP of other host
    sendPort = add_port_list[1] #Port of other host

#Create TCP sockets
sendSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket.listen(1) #Listen for incoming connections
connectionSocket = None #connectionSocket was declared here to make sure program doesn't get stuck on .accept() in while loop using if statement

try:
    #App will try to connect to other host if they are on
    if(add_port_list):
        nothing_happens = 'List is not empty continue through code'
    else:
        raise Exception('List is empty, cannot connect to other host')
    sendSocket.connect((serverIP, sendPort))
    sender = 'From User1: ' #This signifies that this is User2 and the sender is User1
    print('Client found, waiting for message')
except:
    #If app couldn't connect to other host it will be designated as User1
    sender = 'From User2: ' #This signifies that this is User1 and the sender is User2
    print('Cannot find client to connect to, \"Enter your message:\" will appear once client is found')
while True:
    #If statment here to make sure that we don't get stuck in .accept() after accepting the connection the first time
    if(connectionSocket == None):
        connectionSocket, addr = recieveSocket.accept()
    if(add_port_list):
        nothing_happens = 'List is not empty continue through code'
    else: #getting here means the second host connected to the first host, first host now contacts tracker to get info on second host
        trackerSendSocket.connect((trackerIP, trackerPort)) #Connect to tracker, getting here means tracker is already on, no need to check
        trackerSendSocket.send(str(recievePort).encode()) #Send port number to tracker, sent as string to call .encode()
        str_list = trackerSendSocket.recv(1024).decode('utf-8') #Recieve list containing other host's IP and port
        add_port_list = eval(str_list) #Since tracker sends list as string, we convert it back to list here
        serverIP = add_port_list[0] #IP of other host
        sendPort = add_port_list[1] #Port of other host
    #This part of the code will be run if the user is designated as User2
    if(sender == 'From User1: '):
        try:
            sendSocket.connect((serverIP, sendPort))
        except:
            exception = 'exception happened'
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
        word = input('Enter your message: ') #User1 sends first
        #Since at the beginning User1 won't be connected to User2, it will try to connect to it here
        try:
            sendSocket.connect((serverIP, sendPort))
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
The app takes tracker ip, and tracker port as arguments before running the app
The whole system (apps and tracker) are implemented in a way such that there can be a max of two apps, adding a third will register on the tracker
but will mess up the apps and they won't work correctly

IMPORTANT
Launch one app first and wait until 'Cannot find client to connect to, "Enter your message:" will appear once client is found' prints, it may take a moment (20secs to 1min)
If you don't wait until it prints then the apps will not run as intended
after 'Cannot find client to connect to, "Enter your message:" will appear once client is found' is printed you can run the second app
then the second app will print 'Client found, waiting for message' and the first app will have "Enter your message: "
after that the apps will work as intended with the first app launched being the one that sends first

To exit, exit message must all be in lower case
'''
