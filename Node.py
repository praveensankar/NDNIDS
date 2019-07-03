from Face import Face
from ContentStore import ContentStore
from PendingInterestTable import PendingInterestTable
from ForwardingInformationBase import ForwardingInformationBase
from Name import Name
from Transport import Transport
from Interest import Interest
from IDS import IDS
import multiprocessing
import time

class Node:
    """
    Defines the Node in the ndn architecture

    The node contains the content store, pending interest table (PIT), forwarding information base (FIB) and the
    list of faces.
    id - Each node will have unique id
    name - Each node will have unique name ( object of the Name class)
    Content store - caches the incoming data to satisfy the future requests
    Pending Interest Table - contains the list of pending interests
    Forwarding Information Base - contains the forwarding strategy
    Faces - will enable communication between nodes and between node and application


    eg:-
    from Node import Node
    from Name import Name
    from Data import Data
    from Face import Face
    id = 1
    name = Name("node")
    node = Node(id, name)
    print(node)
    print(node.get())
    print(node.get_value())
    print(node.get_id())
    print(node.get_name())
    print(node.get_content_store())

    name1 = Name("name1")
    name2 = Name("name2")
    data1 = Data(name1, "data1")
    data2 = Data(name2, "data2")
    cs = node.get_content_store()
    cs.add(name1,data1)
    cs.add(name2,data2)
    print(node.get_content_store())
    print(node.get_pending_interest_table())

    face1 = Face("face1")
    face2 = Face("face2")
    pit = node.get_pending_interest_table()
    pit.add(name1,face1)
    pit.add(name1,face2)
    print(node.get_pending_interest_table())
    faces = node.get_faces()
    print(node.check_face(faces[0]))
    print(node.get_face(faces[0].get_id()))
    """


    def __init__(self, id = 0, name = None, content_store = None, pending_interest_table = None, forwarding_information_base = None,
                 faces = None):
        self.__id = id
        self.__name = name
        self.__content_store = ContentStore()
        self.__pending_interest_table = PendingInterestTable()
        self.__forwarding_information_base = ForwardingInformationBase()
        self.__faces = []
         # by default 2 faces will be created
        self.create_faces()


    def __str__(self):
        node = self.get()
        return str(node)

    def get(self):
        id = self.get_id()
        name = self.get_name()
        cs = self.get_content_store()
        pit = self.get_pending_interest_table()
        fib = self.get_forwarding_information_base()
        faces = self.get_faces()
        node = {"id" : id, "name" : name, "content_store" : cs, "pending_interest_table" : pit,
                "forwarding_information_base": fib, "faces" : faces}
        return node

    def get_value(self):
        id = self.get_id()
        name = self.get_name().get_value()
        cs = self.get_content_store().get_value()
        pit = self.get_pending_interest_table().get_value()
        fib = self.get_forwarding_information_base().get_value()
        faces = []
        for  face in self.get_faces():
            faces.append(face.get_value())
        node = {"id": id, "name": name, "content_store": cs, "pending_interest_table": pit,
                "forwarding_information_base": fib, "faces": faces}
        return node


    def get_id(self):
        return self.__id

    def set_id(self, id = None):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name = None):
        self.__name = name


    def get_content_store(self):
        return self.__content_store


    def set_content_store(self, content_store):
        self.__content_store = content_store


    def get_pending_interest_table(self):
        return self.__pending_interest_table


    def set_pending_interest_table(self, pending_interest_table = None):
        self.__pending_interest_table = pending_interest_table


    def get_forwarding_information_base(self):
        return self.__forwarding_information_base


    def set_forwarding_information_base(self, forwarding_information_base = None):
        self.__forwarding_information_base = forwarding_information_base


    def get_faces(self):
        """
        Returns the list of the faces object
        """
        return self.__faces


    def get_all_faces(self):
        """
        Returns the list of faces (id, name)
        """
        faces = self.get_faces()
        res = []
        for face in faces:
            res.append(face.get_value())
        return res

    def get_all_faces_values(self):
        """
        Returns the face id, name, {ip_addr,port}
        """

        faces = self.get_faces()
        res = []
        for face in faces:
            res.append(face.get())
        return res

    def check_face(self, face):
        """
        checks whether the node contains the face with given id or name
        """

        return face in self.get_faces()

    def check_face_by_id(self, face):
        faces =self.get_faces()
        for f in faces:
            if f.get_id() == face.get_id():
                return True
        return False

    def get_face(self, id = None):
        """
        face - id of the face (it is an integer)
        """

        faces = self.get_faces()
        for face in faces:
            face_id = face.get_id()
            if id == face_id:
                return face
        else:
            return None


    def add_face(self, id = 0, name = "test face"):
        """
        Adds face (network interfaces) to the node.
        face - object of the Face class
        :param id: id of the face
        :param name: name of the face
        :return: true if face is added to the node and false if it not.
        """
        face = Face(id, name,'127.0.0.1', self)
        try:
            if not isinstance(face, Face):
                raise TypeError("face object is incorrect")
            else:
                self.__faces.append(face)
                return True
        except TypeError:
            print("incorrect face object")
            return False


    def create_faces(self):
        """
        this method creates the faces for the node. Then all the faces will be added to the node.
        By default 2 - number of faces will be created.
        Todo: Create a function which can customize the create_faces for the nodes
        """
        # faces will have ids 1, 2, 3, 4
        # names of the faces will be - face1, face2, face3, face4
        n = 2
        ids = [x for x in range(1,n+1)]
        names = ["face"+str(id) for id in ids]

        for i in range(n):
            self.add_face(ids[i], names[i])


    def send_interest(self, face, interest):
        """
        Receive interest from the face (applications will send interest)
        Entry will be added in the pit table
        interest will be forwarded to all the faces in the node except the incoming face
        """

        self.process_interest(face, interest)


    def forward_interest(self):
        """
        Forward interest from node ( forwarding daemon ) to application / networking interfaces through face
        """
        pass


    # def run_faces(self):
    #     """
    #     Run faces in the background
    #     """
    #     faces = self.get_faces()
    #     mp1 = multiprocessing.Process(target=faces[0].listen(),  daemon=True)
    #
    #     mp2 = multiprocessing.Process(target=faces[1].listen(), daemon=True)
    #     mp1.start()
    #     mp2.start()

    def process_interest(self, face, interest):
        """
        Receive interest from the
        """
        try:
            if self.check_face(face):
                try:

                    if isinstance(interest, Interest):

                        #Todo check whether content store has the data for the incoming interest
                        name = interest.get_name()
                        cs = self.get_content_store()

                        if cs.check_name(name):
                            data = cs.get_data(name)

                            #send this data to the consumer
                            self.send_data(face, data)
                            return True
                        # add entry in the PIT
                        pit = self.get_pending_interest_table()
                        pit.add(name, face)

                        # forward to all faces except the incoming face
                        faces = self.get_faces()
                        for f in faces:
                            if f == faces:
                                continue
                            else:
                                f.forward_interest(interest)

                        return True
                    else:
                        raise ValueError("incorrect interest format")

                except ValueError:
                    return  False
            else:
                raise ValueError("incorrect face object")

        except ValueError:
            return False


    def send_data(self, face, data):
        """
        send data from node to the the application through face
        """
        face.forward_data(data)

    def forward_data(self):
        """
        Forward data from node ( forwarding daemon ) to application / networking interfaces through face
        """
        pass

    def receive_data(self, data, incoming_face):
        """
        Receive data from the networking interfaces or application through face
        Add the data to the content store
        If there is any pending interest for the data is remaining then send the data to the face.
        Todo : Add the incoming face to the fib along with the name prefix.
        """

        """
        If the incoming data is safety message, send it to intrusion detection system and forward it to all
        the faces.
        """
        data_type = data.get_content().get_tlv_type()
        if data_type in range(128,138):
            self.process_safety_message(data, incoming_face)
            name = data.get_name()
            cs = self.get_content_store()
            cs.add(name, data)
            return True



        pit = self.get_pending_interest_table()
        pending_interests = pit.get_all_interests()
        name = data.get_name()
        if pit.check_name_prefix(name):
            face_ids = pit.get_faces(name)
            for id in face_ids:
                face = self.get_face(id)
                self.send_data(face, data)
            pit.remove(name)
        cs = self.get_content_store()
        cs.add(Name(name), data)


    def process_safety_message(self, data, incoming_face):
        """
        Todo : Implement IDS
        :param data: Data object. This is the safety message.
        :param incoming_face: This is the incoming face.
        :return:
        """

        # get one more dummy data packet which contains all the sensor values
        # It will wait for half seconds so it will cause impact on the performance
        time.sleep(0.5)
        dummy_data = incoming_face.get_dummy_data()
        # forward the data all faces except the incoming face
        if self.get_ids().process(data, dummy_data, self) is False:
            print("fake message")
            print("*" * 100)
            return False
        print("genuine message")
        print("*" * 100)
        faces = self.get_faces()
        for face in faces:
            if face.get_value() == incoming_face.get_value():
                continue
            else:
                self.send_data(face, data)

    def attach_IDS(self, ids):
        """

        :param ids: IDS object. attach ids to the node
        :return:
        """

        self.__ids = ids

    def get_ids(self):
        return self.__ids

    def set_ids(self, ids):
        self.attach_IDS(ids)







