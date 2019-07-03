from Core import Core
from Face import Face
from Keys import Keys
from Interest import Interest
from Name import Name
from Data import Data
import time
import pickle
import socket

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
time.sleep(1)
while True:
   data,addr = client_socket.recvfrom(10240)
   data = pickle.loads(data)
   break


print(data.get_value())

client_socket.close()
