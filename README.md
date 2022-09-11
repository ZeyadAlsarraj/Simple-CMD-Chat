# Simple-CMD-Chat
A Couple versions of a simple cmd based chat app that have users take turns in sending messages to each other, each version is implemented in a different way to achieve the same goal.

chat versions only work with the same version, on different physical devices, and connected to the same local area network.

operation is as follows:
1- Run chat version through cmd on one device, providing relevant ip addresses and port numbers if needed. Note for v2, tracker needs to be running first and requires a third device.
2- Run same chat version on another device and it should connect
3- First device gets the first turn in sending messages and turns alternate.
4- After any of the two communicating parties sends the word "exit" both programs terminate.

## chat_v1:
Simplest implementation. To run it requires the user to provide the port number that will be used, the other host's ip address, and the other host's port number.

example: python chat_v1.py 12345 192.168.222.222 54321

## chat_v2:
Tracker implementation. To run a Third device called a tracker is needed which records devices that connect to it and sends the information of the devices connected to one device so it can initiate a connection to begin the chat. To run it needs the tracker's ip address and tracker's port number.

example: python chat_v2.py 192.168.222.222 12345

## chat_v3:
Port scanning implementation. To run it requires the user to provide the ip address of the other host and the program will create threads to look for the port number of the other device if it is on.

example: python chat_v3.py 192.168.222.222
