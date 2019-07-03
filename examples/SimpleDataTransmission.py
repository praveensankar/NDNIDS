from NDN.Core import Core
from NDN.Face import Face
from NDN.Keys import Keys
from NDN.Interest import Interest
from NDN.Name import Name
from NDN.Data import Data
import time
import pickle
import socket
node = Core.get()
faces = Core.get_all_faces()
print(faces)
face = Core.get_face(1)
print(face.get())

key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()
name = "name3"
interest = Interest(name)
interest.set_signature(private_key)

transport = face.get_transport()
ip = transport.get_ip()
port = transport.get_port()
face_address = (ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1',0))
#transport.receive_interest(interest)
#face.send_interest(interest)
time.sleep(1)
client_socket.sendto(pickle.dumps(interest),face_address)
time.sleep(1)
name = "name3"
content = "welcome to the world of programming"
mydata = Data(name,content)
mydata.set_signature(private_key)
client_socket.sendto(pickle.dumps(mydata),face_address)
while True:
   data,addr = client_socket.recvfrom(10240)
   data = pickle.loads(data)
   break


print(data.get_value())

client_socket.close()
