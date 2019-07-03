
from Name import Name
from TLV import TLV
from DataSignature import DataSignature
from Sensor import Sensor
class Data:
    """
    Defines the Data

    eg:-
    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    name = "myname"
    content = "welcome to the world of programming"
    data = Data(name,content)
    for k,v in data.get().items():
        print(k,v.get_value())
    data.set_signature(private_key)
    print(data.get_signature().get_value())
    print(data.verify_signature(public_key))
    """

    def __init__(self,name=None,value=None):
        """
        name: producer can choose name for the data ( object of the Name class)
        value: this is the actual content

        Todo: In the meta_info add content type, freshness period and final block id
        """

        self.__content_type = TLV(24, 1024, "content type")
        self.__meta_info = TLV(20, 1024, "meta info")
        self.__name = name
        self.__sensors = Sensor().get()
        self.__content = TLV(21, 10240, value)
        self.__data_signature = DataSignature()


    def __str__(self):
        """


        """
        content_type = self.get_content_type()
        meta_info = self.get_meta_info()
        name = self.get_name()
        content =self.get_content()
        signature = self.get_signature()
        data = {"content_type" : content_type, "meta_info" : meta_info, "name" : name,
                "content" : content, "signature" : signature}
        return str(data)


    def get_content_type(self):
        return self.__content_type


    def get_meta_info(self):
        return self.__meta_info



    def get_name(self):
        return self.__name


    def get_content(self):
        return self.__content


    def get_signature(self):
        return  self.__data_signature

    def get_sensors(self):
        return self.__sensors

    def set_sensors(self, sensors):
        """
        sensors - It is the object of the Sensors class
        """
        self.__sensors = sensors.get()


    def get_data(self):
        """
         all the fields will be passed as key,value pairs in dictionary
        To examine the contents loop through the dictionary and for each values in the dictionary get tlv value from
        tlv class.
        :return: data dictionary
        """
        content_type = self.get_content_type()
        meta_info = self.get_meta_info()
        name = self.get_name()
        content = self.get_content()
        signature = self.get_signature()
        sensors = self.get_sensors()
        data = {"content_type" : content_type, "meta_info" : meta_info, "name" : name,
                "content" : content, "signature" : signature , "sensors" : sensors}
        return data

    def get(self):
        return self.get_data()


    def get_value(self):
        """

        :return: returns the main content (tlv value of the data)
        """
        data = self.get_content().get_value()
        return data


    def set_content_tye(self, content_type):
        type = TLV(24, 1024, content_type)
        self.__content_type = type

    def set_meta_info(self,info):
        self.__meta_info = TLV(20, 1024, info)

    def set_name(self, name):
        self.__name = name

    def set_content(self, content, tlv = None):
        if tlv is None:
            self.__content = TLV(21, 10240, content)
        else:
            self.__content = tlv

    def set_signature(self, private_key):
        """
        signs the content (tlv value in tlv object) in this object using the user's private key

        :param private_key: private key of the user
        :return: None
        """
        data = self.get_content().get_value()
        self.__data_signature.set_signature(data, private_key)


    def verify_signature(self, public_key):
        signature = self.get_signature()
        data = self.get_content().get_value()
        return signature.verify_signature(data, public_key)





