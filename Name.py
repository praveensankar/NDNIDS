
from TLV import TLV


class Name:
    """
    Defines the Name
    eg:-
    name = Name("name")

    """

    def __init__(self,name):
        """
        name is represented using a 2-level TLV
        outer TLV identifies that it is a name component it has type number 7
        inner TLV contains the actual name component
        3 types of name components : GenericNameComponent, ImplicitSha256DigestComponent,ParametersSha256DigestComponent
        GenericNameComponent is chosen as default
        GenericNameComponent is identified by the type number 8
        for type number assignments refer http://named-data.net/doc/NDN-packet-spec/current/types.html

        :param name: this is the name str
        """
        self.__name_type = TLV(7,1024,"name")
        self.__name_component = TLV(8,1024,name)


    def __str__(self):
        return self.get_name()


    def get_uri(self):
        """
        Creates the URL from the TLV
        :return: returns the URL of the name
        """
        name=self.get_name()
        url="/"+name+"/"
        return  url


    def get_name_component(self):
        """
        :return: returns the name component
        """
        return self.__name_component


    def get_name_type(self):
        return  self.__name_type


    def get_name(self):
        return self.get_name_component().get_tlv_value()

    def get(self):
        return self.get_name_component()


    def get_value(self):
        """

        :return: returns the name
        """
        return self.get_name()