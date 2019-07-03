from NDN.SafetyMessage import SafetyMessage
from NDN.Keys import Keys
from NDN.Name import Name
from NDN.SafetyMessage import SafetyMessageTLV

"""
This file is used to check the working of all the ten safety messages
"""
safety_message_tlvs = SafetyMessageTLV.tlvs
safety_messages = [ "EEBL", "PCN","RHCN","RFN","SVA","CCW" ,"CVW","CRN" ,"CL" ,"EVA" ]
key = Keys()
private_key=key.get_private_key()
public_key=key.get_public_key()
print(public_key)



while True:
   type = int(input("Please enter \n1 to send EEBL\t 2 to send PCN\t 3 to send RHCN"
                    "\t4 to send RFN\t 5 to send SVA\n 6 to send CCW\t 7 to send CVW"
                    "\t8 to send CRN\t 9 to send CL\t 10 to send EVA\t : "))
   if type not in range(1,11):
      break
   sm_type = safety_messages[type - 1]
   name = "/"+str(public_key)+ sm_type
   content = f"this is {sm_type} message"

   # user's public key and safety message type
   sm = SafetyMessage(Name(name), content, sm_type)
   sm.set_signature(private_key)
   print("safety_message  : "+sm.get_content())

