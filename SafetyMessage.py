from Data import Data
from TLV import TLV
class SafetyMessage(Data):


    safety_messages = ["EEBL", "PCN", "RHCN", "RFN", "SVA", "CCW", "CVW", "CRN", "CL", "EVA"]

    def __init__(self, name, content, type):
        """

        :param name: Name class object. It is the name of the safety_message eg:; /user_public_key/message_type
        :param content: str .This is the message content
        :param type: string. This is one of ten safety message types
        """
        super().__init__(name, content)

        #get the sensor values for the safety message
        self.set_content(content, TLV(SafetyMessageTLV.tlvs[type], 4096, content))



    def get_sensor_values(self):
        """
        Returns the sensor value depends on the message type
        """
        pass





class SafetyMessageTLV:
    """
    Use tlv numbers from 128 to 137 for safety messages
    EEBL - Emergency Electronic Brake Light
    PCN  - Post Crash Notification
    RHCN - Road Hazard Condition Notification
    RFN  - Road Feature Notification
    SVA  - Stopped / slow Vehicle Advisor
    CCW  - Cooperative Collision Warning
    CVW  - Cooperative Violation Warning
    CRN  - Congested Road Notification
    CL   - Change of Lanes
    EVA  - Emergency Vehicle Approaching
    """
    tlvs = {
    "EEBL" : 128,
    "PCN" : 129,
    "RHCN" : 130,
    "RFN" : 131,
    "SVA" : 132,
    "CCW" : 133,
    "CVW" : 134,
    "CRN" : 135,
    "CL" : 136,
    "EVA" : 137
    }


