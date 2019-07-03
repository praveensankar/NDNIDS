from Transport import  Transport

class Face:
    """
    Defines the face class

    Each node will contain one or more faces

    eg:-
    from Face import Face
    from Transport import Transport

    id = 1
    name = "face1"
    localhost = '127.0.0.1'
    transport = Transport()
    transport.set('127.0.0.1')
    face = Face(id, name, transport)
    print(face)
    print(face.get())
    print(face.get_value())
    """

    def __init__(self, id = 0, name = "test face", ip_address = None, node = None):
        """
        id - this is the id of the face in the node
        name - this is the name of the face
        transport - this is the networking interface of this face
        """
        self.__id = id
        self.__name = name
        self.__node = node
        self.__transport = Transport(ip_address = ip_address, face = self)



    def __str__(self):
        face = self.get()
        return str(face)


    def get_id(self):
        return self.__id


    def get_name(self):
        return self.__name


    def get_transport(self):
        return self.__transport

    def get_node(self):
        return self.__node


    def set_transport(self, transport = None):
        """
        :param transport: It is the object of the Transport class
        :return: True if successful
        """

        try:
            if isinstance(transport, Transport):
                self.__transport = transport
                return True
            else:
                raise TypeError("invalid transport")
        except TypeError:
            print("incorrect transport format")
            return False


    def get(self):
        id = self.get_id()
        name = self.get_name()
        trasport = self.get_transport().get_value()

        face = {"id" : id, "name" : name, "transport" : trasport}
        return face


    def get_value(self):
        """
        returns the face id
        """
        return self.get_id()

    def send_interest(self, interest):
        """
        send interest from application to the node ( forwarding daemon)
        """
        node = self.get_node()
        node.send_interest(self, interest)



    def forward_interest(self, interest):
        """
        Forward interest from node ( forwarding daemon ) to application / networking interfaces
        """
        transport = self.get_transport()
        transport.send_interest(interest)

    def receive_interest(self, interest):
        """
        Receive interest from the networking interfaces
        """
        node = self.get_node()
        node.receive_interest()

    def send_data(self):
        """
        send data from application to the node ( forwarding daemon)
        """
        pass

    def forward_data(self, data):
        """
        Forward data from node ( forwarding daemon ) to application / networking interfaces
        """
        transport = self.get_transport()
        transport.send_data(data)

    def receive_data(self, data):
        """
        Receive data from the networking interfaces or application and pass it to node
        """
        node = self.get_node()
        node.receive_data(data, self)


    def listen(self):
        self.__transport.listen()


    def get_dummy_data(self):
        """
        Get dummy data from the sender so that safety messages can be verified properly.
        :return: Data object
        """
        transport = self.get_transport()
        data = transport.get_dummy_data()
        return data

