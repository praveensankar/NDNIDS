from Crypto.PublicKey import RSA


class Keys:
    """
    private and public keys are generated
    eg:-
    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    print(private_key)
    print(public_key)
    """

    def __init__(self):
        self.__public_key = None
        self.__private_key = None
        self.__generate_keys()

    @classmethod
    def info():
        return "RSA private / public keys"

    def __str__(self):
        return "RSA private / public keys"

    def __generate_keys(self):

        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open("private.der", "wb")
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open("public_key.der", "wb")
        file_out.write(public_key)
        file_out.close()

        self.__private_key = RSA.import_key(open('private.der').read())
        self.__public_key = RSA.import_key(open('public_key.der').read())


    def set_keys(self,public_key, private_key):
        self.set_public_key(public_key)
        self.set_private_key(private_key)


    def get_public_key(self):
        return self.__public_key


    def set_public_key(self, public_key):
        self.__public_key = public_key


    def get_private_key(self):
        return self.__private_key


    def set_private_key(self, private_key):
        self.__private_key = private_key



