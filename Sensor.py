import random

class Sensor:

    def __init__(self):
        """
        Initialize the sensor
        """
        self.__gps = None
        self.__speed = None
        self.__heartbeat = None
        self.__airbag = None
        #self.refresh_gps()
        self.set_gps()
        self.set_speed()
        self.set_heartbeat()
        self.set_airbag()
        pass

    def get(self):
        """
        Returns the sensor values
        """
        gps = self.get_gps()
        speed = self.get_speed()
        heartbeat = self.get_heartbeat()
        airbag = self.get_airbag()
        sensors = {"gps" : gps, "speed" : speed, "heartbeat" : heartbeat, "airbag" : airbag}
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

    def refresh_gps(self):
        """
        Get gps values from the gps
        """
        import geocoder
        self.__gps = geocoder.ip('me').latlng

        #


    def set_gps(self, latitude = None, longitude = None):
        """
        set dummy gps value
        """
        if latitude is None and longitude is None:
            self.__gps = [random.randint(0,90), random.randint(0,180)]
        if latitude is not None and longitude is not None:
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