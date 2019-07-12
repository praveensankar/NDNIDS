from Data import Data
from geopy.distance import geodesic
import random
class IDS:


    def __init__(self):
        pass

    def __str__(self):
        return "IDS"

    def process(self, data, dummy_data, node):
        """
        It checks all the rules.
        :param data: Data object
        :param dummy_data: Data object
        :param node: Node object
        :return: True if no intrusion and False if intrusion is detected
        """
        print("*" * 100)
        print(f"{data.get_value()} message from {data.get_signature().get_value()}")

        vehicle_movement = True
        speed_reduction = True
        heart_rate = True
        air_bag = True
        total_messages = 0
        genuine_messages = 0
        fake_messages = 0
        with open('total_messages.txt', 'r') as file:
            total_messages = file.read()
            total_messages = int(total_messages)

        with open('genuine_messages.txt', 'r') as file:
            genuine_messages = file.read()
            genuine_messages = int(genuine_messages)

        with open('fake_messages.txt', 'r') as file:
            fake_messages = file.read()
            fake_messages = int(fake_messages)


        data_type = data.get_content().get_tlv_type()

        if data_type in [128, 130, 131, 132, 134]:
            vehicle_movement =  self.check_vehicle_movement(data, node)

        if data_type in [131, 132, 133, 134]:
            #n = random.randint(20,50)
            n=30
            print(f"speed reduction percentage : {n}")
            speed_reduction = self.check_speed_reduction( data, dummy_data, n, node)

        if data_type in [128, 129, 130, 135]:
            #n = random.randint(60,90)
            n=95
            print(f"speed reduction percentage : {n}")
            speed_reduction = self.check_speed_reduction(data, dummy_data, n, node)

        if data_type in [128, 129]:
            heart_rate = self.check_heart_rate( data, node)

        if data_type == 129:
            air_bag = self.check_airbag_status(data)

        genuine_message = vehicle_movement and speed_reduction and heart_rate and air_bag

        if genuine_message is True:
            genuine_messages = genuine_messages + 1
        else:
            fake_messages = fake_messages + 1
        total_messages = total_messages + 1
        print(f"\ntotal messages: {total_messages}\t genuine messages : {genuine_messages}\t fake messages : {fake_messages}")


        with open('total_messages.txt', 'w') as file:
            file.write(str(total_messages))
        with open('genuine_messages.txt', 'w') as file:
            file.write(str(genuine_messages))
        with open('fake_messages.txt', 'w') as file:
            file.write(str(fake_messages))

        return genuine_message

    def check_vehicle_movement(self, data, node):
        """

        :param data: Data object.
        :param node: Node object
        :return:
        """
        name = data.get_name().get_value()
        gps= data.get_sensors()["gps"]
        print("GPS : ", gps)
        gps_history = []
        name_prefix = self.get_name_prefix(name)

        try:

            cs = node.get_content_store()
            data = cs.get_data_by_name(name_prefix)


            for d in data:
                old_gps = d.get_sensors()["gps"]
                print(f"IDS : Data -> {d.get_value()} , gps ->  {old_gps}")


                #vehicle should have moved atlest 100 meters
                dis = geodesic(gps, old_gps).m
                if  dis< 0.031:
                    print(f"Invalid gps ---->  {dis} is less than 100 meters")
                    return False

        except ValueError:
            print("node is not in the correct format")
            return False

        return True


    def check_speed_reduction(self, data = None, dummy_data = None, n = None, node = None):
        """
        It stores the current speed and get one more dummy message from the sender.
        It will compare both speeds and return true if new speed is reduced n%.
        :param data: Data Object
        :param dummy_data: Data Object.
        :param n: percentage of speed to be reduced from the first message to next
        "param node : Node object
        :return:
        """
        speed1 = data.get_sensors()["speed"]
        speed2 = dummy_data.get_sensors()["speed"]
        print(f" speed1 : {speed1}  speed2 : {speed2}")

        if n is None:
            if speed2 < speed1:
                return True
            else:
                print(f"Invalid speed ----> speed2 : {speed2} should be less than  speed1 : {speed1}")
                return False
        if speed2 <= (speed1 - (speed1 * n/100)):
            return True
        else:
            print(f"Invalid speed ----> speed2 : {speed2} should be less than {(speed1 - (speed1 * n/100))}")
            return False


    def check_heart_rate(self, data, node):
        """
        It will check whether the heart rate is increased or not. units -  Beats per Minute
        :return: True if increased and false it is decreased.
        """

        name = data.get_name().get_value()
        heart_rate = data.get_sensors()["heartbeat"]
        print("heart rate : ", heart_rate)
        avg_heart_rate = 0
        count = 0
        name_prefix = self.get_name_prefix(name)

        cs = node.get_content_store()
        history = cs.get_data_by_name(name_prefix)
        for d in history:
                old_heart_rate = d.get_sensors()["heartbeat"]
                print(f"IDS : Data -> {d.get_value()} , heart_rate ->  {old_heart_rate}")
                avg_heart_rate = avg_heart_rate + old_heart_rate
                count = count + 1

        if count == 0:
            if heart_rate > 100:
                return True
            else:
                print(f"Invalid heart_rate ----> heart_rate is {heart_rate} should be greater than 100 BPM")
                return False

        if count > 0:
            avg_heart_rate = avg_heart_rate / count
            print(f"average heart rate : {avg_heart_rate}")
            if heart_rate > avg_heart_rate:
                return True
            else:
                print(f"Invalid heart_rate ----> heart_rate is {heart_rate} should be greater than {avg_heart_rate}")
                return False


    def check_airbag_status(self, data):
        """

        :param data: Data
        :return: True if airbag is triggered and false if not
        """
        airbag_status = data.get_sensors()["airbag"]
        print(f"airbag_status : {airbag_status}")
        if airbag_status == 1:
            return True
        else:
            print("Invalid airbag_status ----> airbag is not triggered ")
            return False

    def get_name_prefix(self, name):
        """

        :param name: str
        :return: str
        """
        name_prefix = ['/']

        for i in range(1, len(name)):
            if name[i] == '/':
                break
            else:
                name_prefix.append(name[i])

        name_prefix = "".join(name_prefix)
        return name_prefix
