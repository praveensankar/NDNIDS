
from Signature import Signature
from TLV import TLV

class InterestSignature:
    """
    Defines interest signature for ndn intereset
    eg:-
    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    interest = "test"
    interest_signaturet=InterestSignature()
    interest_signaturet.set_signature(interest,private_key)
    print(interest_signaturet.get_value())
    claim=interest_signaturet.verify_signature(interest,public_key)
    print(claim)
    """

    def __init__(self):
        """
        signature_info : describes the signature, signature algorithm and other relevant information needed for signature
        signature_value : digital signature of the data
        tlv numbers 44 - signature info 46 - signature value
        """
        self.__signature_info = TLV(44, 1024, "will be set later")
        self.__signature_value = TLV(46, 1024, "wil be set later")


    def __str__(self):
        return str(self.get_signature())


    def get_signature_info(self):
        return self.__signature_info

    def get_signature_value(self):
        return self.__signature_value

    def set_signature_info(self):
        sign_info=Signature.info()
        self.get_signature_info().set_tlv_value(sign_info)

    def set_signature_value(self, interest, private_key):
        """
        It uses set_signature class method in the Signature module to do actual signature
        so different digital signature algorithms can be used without affecting the interest

        :param interest: main content
        :param private_key: private key of the user
        :return: sets the signature value in the object
        """
        signature = Signature.set_signature(interest, private_key)
        self.get_signature_value().set_tlv_value(signature)


    def set_signature(self, interest, private_key):
        self.set_signature_info()
        self.set_signature_value(interest, private_key)


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


    def verify_signature(self, interest, public_key):
        signature = self.get_value()
        claim = Signature.verify_signature(interest, signature, public_key)
        return claim