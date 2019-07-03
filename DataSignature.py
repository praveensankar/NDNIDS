
from Signature import Signature
from TLV import TLV

class DataSignature:
    """
    Defines data signature for ndn data
    eg:-
    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    data = "test"
    ds = DataSignature()
    ds.set_signature(data,private_key)
    print(ds.get_value())
    claim=ds.verify_signature(data,public_key)
    print(claim)
    """

    def __init__(self):
        """
        signature_info : describes the signature, signature algorithm and other relevant information needed for signature
        signature_value : digital signature of the data
        tlv numbers 22 - signature info 23 - signature value
        """
        self.__signature_info = TLV(22, 1024, "will be set later")
        self.__signature_value = TLV(23, 1024, "wil be set later")


    def __str__(self):
        return str(self.get_signature())


    def get_signature_info(self):
        return self.__signature_info

    def get_signature_value(self):
        return self.__signature_value

    def set_signature_info(self):
        sign_info=Signature.info()
        self.get_signature_info().set_tlv_value(sign_info)

    def set_signature_value(self, data, private_key):
        """
        It uses set_signature class method in the Signature module to do actual signature
        so different digital signature algorithms can be used without affecting the data

        :param data: main content
        :param private_key: private key of the user
        :return: sets the signature value in the object
        """
        signature = Signature.set_signature(data, private_key)
        self.get_signature_value().set_tlv_value(signature)


    def set_signature(self, data, private_key):
        self.set_signature_info()
        self.set_signature_value(data, private_key)


    def get_signature(self):
        signature_info = self.get_signature_info()
        signature_value = self.get_signature_value()
        signature = {"signature_info" : signature_info, "signature_value" : signature_value }
        return signature


    def get(self):
        """

        :return: Returns the main content of this object
        """
        return self.get_signature()


    def get_value(self):
        """

        :return: returns the signature of the data
        """
        return self.get_signature_value().get_value()


    def verify_signature(self, data, public_key):
        signature = self.get_value()
        claim = Signature.verify_signature(data, signature, public_key)
        return claim