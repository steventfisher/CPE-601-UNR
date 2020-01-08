# Client Server and Cloud Application
NAME: Steven Fisher  
Homework #4

For homework #4 we needed to add the ability to upload our results to the cloud.
I was able to accomplish the creation of the file by the server the transfer of
access token from the server to the client. From there the client uploads the 
data to the cloud document and then sends a push notification to the server
so that the server will download the results.

Issues that I ran into: Difficulty on getting the Oauth working correctly and
                        managing the updating of info for the document in the
                        cloud.

Homework #3
For homework #3 when added the ability to send messages to the other devices.
The sending device executes either a traceroute or ping and then sends the
results to the receiving device.  Then the receving devices writes the data
to a file. After writing the data sends an ACK code back to sending device
to aknowlegde receipt of data.

Issues that I ran into: Difficulty try to determine how to implement with threads
                        decided to implement using processes.

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
                       
                        
Revisions:
* added a menu option for the commands instead of having to type the input by hand (i.e. REGISTER device_ID IP MAC PORT)                    
* modified the numbering for ACK and NACK
