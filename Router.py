from Node import Node
from Name import Name
from Data import Data
import sys
import random
import socket
import pickle
from IDS import IDS

class Router:
    """
    This class runs the router functionalities
    eg:- python Router.py 3015
    """

    def __init__(self, id = None, name = None, node = None):
        """
        :param id : int . Each router will have a unique id
        :param name : string. This is the router name
        :param node: This is the object of the node class. Router will have a node
        """
        self.__id = id
        self.__name = name
        self.__node = node
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_node(self):
        return self.__node

    def set_up(self):
        """Set up the router"""
        self.__node = Node(1, Name(self.__name))
        # for testing purpose
        name1 = Name("/test1")
        name2 = Name("/test2")
        data1 = Data(name1, "This is the test data 1")
        data2 = Data(name2, "This is the test data 2")

        cs = self.__node.get_content_store()
        cs.add(name1, data1)
        cs.add(name2, data2)

        #add IDS in the node
        ids = IDS()
        self.__node.attach_IDS(ids)


    def connect(self, ip_address,port):
        """
        Connect the router to the internet
        """

        router_address = (ip_address, port)
        self.__sock.bind(router_address)


    def start(self):
        """
        Starts the router
        To close the router press ctrl + c
        """

        while True:
            try:
                data , addr =self.__sock.recvfrom(10240)
                data = pickle.loads(data)
                print(f"{data} from {addr}")
                if data == "ping":
                    #when the router receives the ping message it will send the list of available faces
                    node = self.get_node()
                    faces = node.get_all_faces_values()
                    self.__sock.sendto(pickle.dumps(faces),addr)
            except KeyboardInterrupt:
                break
        self.__sock.close()






id = random.randint(1,100000)
port = 3001
name = "test router"
ip_address = "127.0.0.1"

if __name__ == "__main__":
    # command line arguments
    # 1st argument - int. Router port
    # 2nd argument - int. router id
    # 3rd argument - str. Router name
    if len(sys.argv)>1:
        port = int(sys.argv[1])
    if len(sys.argv)>2:
        id = int(sys.argv[2])
    if len(sys.argv)>3:
        name = int(sys.argv[3])

router = Router(id, name)
router.set_up()
router.connect(ip_address,port)
router.start()