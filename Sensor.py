import random
import csv

class Sensor:

    def __init__(self):
        """
        Initialize the sensor
        """
        self.__gps = None
        self.__speed = None
        self.__heartbeat = None
        self.__airbag = None
        self.__timestamp = None
        #self.refresh_gps()
        sensor_number = None

        #after reading a sensor number increment it add store it in the file
        with open('sensor_tracker.txt', 'r') as file:
            sensor_number = file.read()
            sensor_number = int(sensor_number)
        self.set(sensor_number)
        with open('sensor_tracker.txt', 'w') as file:
            file.write(str(sensor_number+1))

    def get(self):
        """
        Returns the sensor values
        """


        gps = self.get_gps()
        speed = self.get_speed()
        heartbeat = self.get_heartbeat()
        airbag = self.get_airbag()
        timestamp = self.get_timestamp()
        sensors = {"gps" : gps, "speed" : speed, "heartbeat" : heartbeat,
                   "airbag" : airbag, "timestamp": timestamp}
        return sensors

    def get_value(self):
        self.get()

    def get_gps(self):
        return self.__gps

    def get_speed(self):
        return self.__speed

    def get_heartbeat(self):
        return self.__heartbeat

    def get_airbag(self):
        return self.__airbag

    def get_timestamp(self):
        return self.__timestamp

    def refresh_gps(self):
        """
        Get gps values from the gps
        """
        import geocoder
        self.__gps = geocoder.ip('me').latlng

        #


    def set(self, sensor_number):
        """

        :param sensor_number: int sensor_number to get the dummy sensor value
        :return: None
        """
        sensor = None
        with open('sensor.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == sensor_number:
                    sensor = row
                    break
                else:
                    line_count += 1
        self.set_gps(float(sensor['latitude']),float(sensor['longitude']))
        self.set_speed(float(sensor['speed']))
        self.set_heartbeat(int(sensor['heartrate']))
        self.set_airbag(int(sensor['airbag']))
        self.set_timestamp(sensor['timestamp'])

    def set_gps(self, latitude = None, longitude = None):
        """
        set dummy gps value
        """
        self.__gps = [latitude, longitude]


    def set_speed(self, speed = None):
        """

        :param speed: int. dummy speed . units - km / h
        :return: None
        """

        if speed is None:
            self.__speed =  random.randint(0, 100)
        else:
            self.__speed = speed


    def set_heartbeat(self, heartbeat = None):
        """

        :param heartbeat: int. units - beats per minute (BPM)
        :return:
        """

        if heartbeat is None:
            self.__heartbeat = random.randint(60,120)
        else:
            self.__heartbeat = heartbeat

    def set_airbag(self, airbag = None):
        """
        Sets air bag sensor.
        :param airbag: int.
        :return: int. 0 - not triggered 1 - triggered
        """
        if airbag is None:
            self.__airbag = random.randint(0,1)
        else:
            self.__airbag = airbag


    def set_timestamp(self, timestamp = None):
        if timestamp is None:
            import time
            self.__timestamp = time.ctime(time.time())
        else:
            self.__timestamp = timestamp