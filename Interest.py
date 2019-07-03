from Name import Name
from TLV import TLV
from InterestSignature import InterestSignature



class Interest:
    """
    Defines the interest

    eg:-

    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    name = "myname"
    interest = Interest(name)
    print(interest)

    for k,v in interest.get().items():
        print(k,v.get_value())
    interest.set_signature(private_key)
    print(interest.get_signature().get_value())
    print(interest.verify_signature(public_key))
    """

    def __init__(self, name, nonce = None, lifetime = None, hop_limit=None):
        self.__name = Name(name)
        self.__nonce = TLV(10, 1024, nonce)
        self.__interest_lifetime = TLV(12, 1024, lifetime)
        self.__hop_limit = TLV(34, 1024, hop_limit)
        self.__interest_signature = InterestSignature()


    def __str__(self):
        """


        """
        name = self.get_name()
        nonce = self.get_nonce()
        interest_lifetime =self.get_interest_lifetime()
        hop_limit = self.get_hop_limit()
        signature = self.get_signature()
        interest = {"name": name, "nonce" : nonce, "interest_lifetime" : interest_lifetime,
                "hop_limit" : hop_limit, "signature": signature}
        return str(interest)


    def get_interest(self):
        """ all the fields will be passed as key,value pairs in dictionary
        To examine the contents loop through the dictionary and for each values in the dictionary get tlv value from
        tlv class.
        :return: interest dictionary
        """
        name = self.get_name()
        nonce = self.get_nonce()
        interest_lifetime = self.get_interest_lifetime()
        hop_limit = self.get_hop_limit()
        signature = self.get_signature()
        interest = {"name": name, "nonce": nonce, "interest_lifetime": interest_lifetime,
                    "hop_limit": hop_limit, "signature": signature}
        return interest

    def get_name(self):
        return self.__name


    def get_nonce(self):
        return self.__nonce


    def get_interest_lifetime(self):
        return self.__interest_lifetime


    def get_hop_limit(self):
        return self.__hop_limit


    def get_signature(self):
        return self.__interest_signature


    def get(self):
        return self.get_interest()


    def get_value(self):
        return self.get_name().get_value()


    def set_name(self, name):
        self.__name = Name(name)


    def set_nonce(self, nonce=None):
        self.__nonce.set_tlv_value(nonce)


    def set_interest_lifetime(self, lifetime = None):
        self.__interest_lifetime.set_tlv_value(lifetime)


    def set_hop_limit(self, hoplimit = None ):
        self.__hop_limit.set_tlv_value(hoplimit)


    def set_signature(self,private_key):
        """
                signs the interest_name (tlv value in tlv object) in this object using the user's private key

                :param private_key: private key of the user
                :return: None
                """
        interest = self.get_value()
        self.__interest_signature.set_signature(interest, private_key)


    def verify_signature(self, public_key):
        signature = self.get_signature()
        interest_name = self.get_value()
        return signature.verify_signature(interest_name, public_key)