'''IMPORTANT INSTRUCTIONS IN A COMMENT AT THE BOTTOM'''
from socket import *
import sys
import argparse

#Create the arguments to be inputted when running program
parser = argparse.ArgumentParser(description = 'Simple python chat app v_1')
parser.add_argument('rcv_port', type = int, metavar = '', help = 'Local port')
parser.add_argument('other_host_ip', type = str, metavar = '', help = 'Other host\'s IP')
parser.add_argument('send_port', type = int, metavar = '', help = 'Other host\'s port')

args = parser.parse_args()

serverIP = args.other_host_ip #IP of other host
recievePort = args.rcv_port #Local host's port
sendPort = args.send_port #Port of other host
#Create TCP sockets
sendSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket = socket(AF_INET, SOCK_STREAM)
recieveSocket.bind(('0.0.0.0', recievePort)) #Bind socket
recieveSocket.listen(1) #Listen for incoming connections
connectionSocket = None #connectionSocket was declared here to make sure program doesn't get stuck on .accept() in while loop using if statement

try:
    #App will try to connect to other host if they are on
    sendSocket.connect((serverIP, sendPort))
    sender = 'From User1: ' #This signifies that this is User2 and the sender is User1
    print('Client found, waiting for message')
except:
    #If app couldn't connect to other host it will be designated as User1run this code
    sender = 'From User2: ' #This signifies that this is User1 and the sender is User2
    print('Cannot find client to connect to, \"Enter your message:\" will appear once client is found')
while True:
    #If statment here to make sure that we don't get stuck in .accept() after accepting the connection the first time
    if(connectionSocket == None):
        connectionSocket, addr = recieveSocket.accept()
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
The app takes local port, other host's IP address, and other host's port as arguments before running the app

IMPORTANT
Launch one app first and wait until 'Cannot find client to connect to, "Enter your message:" will appear once client is found' prints, it may take a moment (20secs to 1min)
If you don't wait until it prints then the apps will not run as intended
after 'Cannot find client to connect to, "Enter your message:" will appear once client is found' is printed you can run the second app
then the second app will print 'Client found, waiting for message' and the first app will have "Enter your message: "
after that the apps will work as intended with the first app launched being the one that sends first
'''
