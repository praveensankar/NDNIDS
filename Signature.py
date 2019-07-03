from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

class Signature:
    """
    this signature is a helper for cryptography related activities and signing the data packet
    eg:-
    key = Keys()
    private_key=key.get_private_key()
    public_key=key.get_public_key()
    print(private_key)
    print(public_key)
    data = "test"
    signature = Signature.set_signature(data, private_key)
    print(signature)
    claim = Signature.verify_signature(data, signature, public_key)
    print(claim)
    """


    @staticmethod
    def info():
        return "SHA-256"

    @staticmethod
    def set_signature(data, private_key):
        """
        SHA-256 is used as a signature algorithm
        private key - private key of the user

        :param data: this is the content data for which signature is needed
        :return: hash value of the message is calculated and the message is signed using private key
        """

        message = data.encode()
        key=private_key
        h = SHA256.new(message)
        signature = pkcs1_15.new(key).sign(h)
        return signature


    @staticmethod
    def verify_signature(data, signature, public_key):
        """
        SHA-256 is used for verifying digital signature
        public key - public key of the user
        :param data: this is the data for which the signature needs to be calculated
        :param signature: this is the signature value
        :return: returns whether the signature of data and signature passed as a argument is same or not.
                 if same the it will return true or else it will return false.
        """

        #key = RSA.import_key(open('public_key.der').read())
        key = public_key
        message = data.encode()
        h = SHA256.new(message)
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False