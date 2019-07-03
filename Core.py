from Node import Node
from Name import Name
from Data import Data
import Port
import socket
import pickle

class Core:
    """
    This class is the interface between the ndn node and the rest of the modules which will use node.
    It creates a single node object and uses it for doing all the tasks.

    eg:-

    """

    faces = None


    @staticmethod
    def get_all_faces():
        """
        send the ping message to the router
        router ip_address and port should be mentioned correctly
        router will send list of faces
        """

        core_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = "ping"
        core_socket.sendto(pickle.dumps(message),('127.0.0.1',Port.port))

        while True:
            data, addr = core_socket.recvfrom(10240)
            data = pickle.loads(data)
            break
        faces = data
        return faces

    @staticmethod
    def get():
        """
        If the node already has an object then that object will be returned
        Or else new object for the node will be created
        """
        return Core.get_all_faces()


    @staticmethod
    def get_face(id = None):
        """

        :param id: Integer id of the face
        :return: Face object
        """
        faces = Core.get_all_faces()
        for face in faces:
            if face["id"] == id:
                return face
        return None

