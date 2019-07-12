"""
This producer sends no_of_safety messages continously to all the consumers
"""

from Core import Core
from Face import Face
from Keys import Keys
from Interest import Interest
from Name import Name
from Data import Data


from SafetyMessage import SafetyMessage
from SafetyMessage import SafetyMessageTLV

import time
import pickle
import socket
import threading


faces = Core.get_all_faces()
face = Core.get_face(1)


key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()

def listen():
    """
    When the face requests for dummy data send dummy data
    :return:
    """
    while True:
        data, addr = client_socket.recvfrom(10240)
        data = pickle.loads(data)
        if data == "dummy":
            name = "/"+str(public_key)+"/dummy/"
            content = "Dummy data"
            mydata = Data(name, content)
            mydata.set_signature(private_key)
            client_socket.sendto(pickle.dumps(mydata), face_address)



# send 25 safety messages
no_of_messages = 300

safety_message_tlvs = SafetyMessageTLV.tlvs
safety_messages = [ "EEBL", "PCN","RHCN","RFN","SVA","CCW" ,"CVW" ,"EVA" ]
key = Keys()
private_key=key.get_private_key()
public_key=key.get_public_key()
print(public_key)


transport = face['transport']
ip=transport['ip_address']
port = transport['port']
face_address = (ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1',0))
#user's public key and safety message type
# mydata = Data("/"+str(public_key)+"/testdata","hi")
# mydata.set_signature(private_key)
# client_socket.sendto(pickle.dumps(mydata),face_address)
# name = "name4"
# content = "welcome to the world of programming"
# mydata = Data(name,content)
# mydata.set_signature(private_key)
# client_socket.sendto(pickle.dumps(mydata),face_address)
#

th = threading.Thread(target=listen, args=())
th.daemon = True
th.start()


for i in range(no_of_messages):

    #type = int(input("Please enter \n1 to send EEBL\t 2 to send PCN\t 3 to send RHCN"
    #               "\t4 to send RFN\t 5 to send SVA\t 6 to send CCW\n 7 to send CVW"
    #               "\t8 to send CRN\t 9 to send CL\t 10 to send EVA\t 11 to produce normal data \t : "))

    #send sva
    type = 8
    if type == 11:
        name = input("Please enter name for the message : ")
        content = input(" please enter the content : ")
        mydata = Data(name, content)
        mydata.set_signature(private_key)
        client_socket.sendto(pickle.dumps(mydata), face_address)
        continue

    if type not in range(1,11):
        break
    sm_type = safety_messages[type - 1]
    name = "/"+str(public_key)+"/"+ sm_type
    content = f"this is {sm_type} message"
    sm = SafetyMessage(Name(name), content, sm_type)
    sm.set_signature(private_key)
    print("safety_message  : "+str(sm.get_content()))
    time.sleep(1)
    client_socket.sendto(pickle.dumps(sm), face_address)




th.join()
client_socket.close()

