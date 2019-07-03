"""
This consumer receives the safety message
"""

from Core import Core
from Face import Face
from Keys import Keys
from Interest import Interest
from Name import Name
from Data import Data
import time
import pickle
import socket
import threading



def listen():
   while True:
      data, addr = client_socket.recvfrom(10240)
      data = pickle.loads(data)
      print("\n"+data.get_value())



faces = Core.get_all_faces()
face = Core.get_face(1)


key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()
name = "name4"
interest = Interest(name)
interest.set_signature(private_key)

transport = face['transport']
ip=transport['ip_address']
port = transport['port']
face_address = (ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1',0))
client_socket.sendto(pickle.dumps(interest),face_address)

th = threading.Thread(target=listen, args=())
th.daemon = True
th.start()
while True:
   # look for data from the producer in the background

   choice = int(input("enter 1 to send interest \t 2 to exit\t: "))
   if choice == 2:
      th.join()
      break
   if choice == 1:
      name = input("please enter the name : ")
      interest = Interest(name)
      interest.set_signature(private_key)
      client_socket.sendto(pickle.dumps(interest), face_address)




client_socket.close()

