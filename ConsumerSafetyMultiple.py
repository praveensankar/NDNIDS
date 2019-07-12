"""
More than one consumers receives the safety message
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



def listen(client_id = None):
   while True:
      data, addr = client_socket[client_id].recvfrom(10240)
      data = pickle.loads(data)
      print(threading.current_thread().getName()+"\t"+data.get_value()+"\n")



faces = Core.get_all_faces()
consumer_faces = []

#10 consumers are being used

no_of_consumers = 10

for i in range(2,no_of_consumers+12):
    consumer_faces.append(Core.get_face(i))

key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()



key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()
client_socket = []
threads = []

face_address = None
for i in range(no_of_consumers):
    face = consumer_faces[i]
    transport = face['transport']
    ip = transport['ip_address']
    port = transport['port']
    face_address = (ip, port)

    client_socket.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    client_socket[i].bind(('127.0.0.1',0))
    name = "name4"
    interest = Interest(name)
    interest.set_signature(private_key)
    client_socket[i].sendto(pickle.dumps(interest),face_address)
    th = threading.Thread(target=listen, args=(i,))
    th.setName("consumer "+str(i))
    th.daemon = True
    threads.append(th)
    th.start()

while True:
   # look for data from the producer in the background

   choice = int(input(" 2 to exit\t: "))
   if choice == 2:
      for thread in threads:
        thread.join()
      break


for client_sock in client_socket:
    client_sock.close()

