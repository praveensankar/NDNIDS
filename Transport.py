import socket
from Data import Data
import multiprocessing
import pickle
from Interest import Interest
import threading
class Transport:
    """
    This class defines the networking interface of the face
    UDP socket is used for transmission
    Each socket will have ip address and port
    eg:-

    from Transport import Transport

    ip = "127.0.0.1"
    port = 5000
    transport = Transport(ip, port)
    print(transport)
    print(transport.get())
    print(transport.get_value())
    t1 = Transport()
    t1.set(ip,5002)
    print(t1.get_value())


    To use system generated ports

    from Transport import Transport
    t = Transport()
    t.set('127.0.0.1')
    print(t.get_value())
    """


    def __init__(self, ip_address = None,  port = None, face = None ):
        """

        :param ip_address: ip address for the face
        :param port: port number for the face
        UDP socket will be used.
        """
        self.__ip_address = ip_address
        self.__port = port
        self.__face = face
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__peer_address = None
        if ip_address is not None and port is not None:
            self.__sock.bind((ip_address, port))
        if ip_address is not None and port is None:
            self.set(ip_address)



    def __str__(self):
        sock = self.get_socket()
        return str(sock)


    def get(self):
        """
        Returns the udp socket
        """
        return self.get_socket()

    def get_value(self):
        """
        Returns ip address and port number
        """
        ip = self.get_ip()
        port = self.get_port()

        address = {"ip_address" : ip, "port" : port}
        return address



    def get_ip(self):
        return self.__ip_address


    def get_port(self):
        return self.__port


    def set_ip(self, ip_address):
        self.__ip_address = ip_address


    def set_port(self, port):
        self.__port = port

    def get_socket(self):
        return self.__sock

    def get_face(self):
        return self.__face


    def set_face(self, face = None):
        self.__face = face

    def set(self, ip_address = None, port = None):
        try:
            if ip_address is None:
                raise ValueError("ip or port is not defined")
            self.set_ip(ip_address)
            if port is None:
                self.__sock.bind((ip_address, 0))
                port = self.__sock.getsockname()[1]
                self.set_port(port)


                #start the listen in background
                th = threading.Thread(target=self.listen, args=())
                th.daemon = True
                th.start()
                return True
        except ValueError:
            print("give ip address and port number")
            return False


    def send_interest(self, interest):
        """
        send interest or data from face to network interface
        """
        pass

    def send_data(self, data):
        """
        send interest or data from face to network interface
        """
        self.__sock.sendto(pickle.dumps(data), self.__peer_address)

    def receive_interest(self, interest = None):
        """
        receive interest or data from the network interface and send it to face

        Todo: I think this should be the one which has to run continuously in the background and whenever
        it receives any packet ,that packet has to be forwarded to the face
        """
        face = self.get_face()
        face.send_interest(interest)

    def receive_data(self, data):
        """
        receive interest or data from the network interface and send it to face

        Todo: I think this should be the one which has to run continuously in the background and whenever
        it receives any packet ,that packet has to be forwarded to the face
        """
        face = self.get_face()
        face.receive_data(data)

    def receive(self, data):
        """

        :param data: This can be either data object or interest object
        :return:
        """
        if isinstance(data, Interest):
            self.receive_interest(data)

        if isinstance(data, Data):
            self.receive_data(data)

    def listen(self):
        """

        :param receive_interest: call the receive_interest function if new interest arrives
        :param receive_data:  call the receive_data function if new data arrives
        :return:
        """
        while True:
            data, addr = self.__sock.recvfrom(10240)
            data = pickle.loads(data)
            #print(data)
            #print(type(data))
            self.__peer_address = addr
            self.receive(data)


        self.__sock.close()


    def get_dummy_data(self):
        """
        Get dummy data from the sender
        :return:
        """
        self.__sock.sendto(pickle.dumps("dummy"), self.__peer_address)
        while True:
            data, addr = self.__sock.recvfrom(10240)
            data = pickle.loads(data)
            #print(data)
            break

        return data
