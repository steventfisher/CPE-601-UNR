# Python TCP Client Server Application
NAME: Steven Fisher  
Homework #2

The code does seem to work. However, you currently need to execute the REGISTER
command after starting the fisher_hw2_client.py script. It takes the input
from the command and enters it into the client database. You are able to query
for devices and messages. Also, you can send messages from one client to 
another. You are also able to deregister a device and use the quit command,
however I was not sure how to log the device off in the server. The activity
log registers when messages are sent to a client. The Error.log registers
the NACK responses that were issued.

Issues that I ran into: 
* Making it so that the client is able to issue more than one command on each run.  
* I also haven't figured out how to code up to make sure that the server/client has received the whole message  
* I also have not figured out how to make the timeout work for REGISTER command  
* I am sure that there are probably other issues that I have not taken care of yet. Such as possible misinterpretation of the way to send and receive some of the commands.  
