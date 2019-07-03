from Name import Name
from Data import Data

class ContentStore:
    """
    defnes the content store

    content_store caches the data that are coming to the node
    It is list of (name, data) pair.
    name is the object of the Name class
    data is the Object of the Data class

    eg:-
    from Data import Data
    from ContentStore import ContentStore
    from Name import Name

    name1 = Name("name1")
    name2 = Name("name2")
    name3 = Name("name3")

    data1 = Data(name1, "data1")
    data2 = Data(name2, "data2")

    cs = ContentStore()
    cs.add(name1,data1)
    cs.add(name2,data2)
    print(cs.get())
    print(cs.get_value())
    print(cs.get_all_names())
    print(cs.get_data(name1))
    print(cs.check_name(name2))
    print(cs.check_name(name3))
    print(cs.check_data(data2))
    print(cs.remove(name2))
    print(cs.get())

    """

    def __init__(self):
        """
        content stores the list of (name,data) pairs. It is a dictionary
        """
        self.__content = {}


    def __str__(self):
        """
        returns the list of name,data as a string
        """
        return str(self.get())


    def get(self):
        """
        Returns the list of (name,data) dictionary object

        """
        content={}
        for name,data in self.__content.items():
            content[name.get_value()] = data.get_value()
        return content


    def get_value(self):
        """
        returns the list of names in content store as a list
        """
        return self.get_all_names()


    def get_all_names(self):
        """
        returns all the names in the content store
        """
        names = []
        content = self.get()
        for name, data in content.items():
            names.append(name)
        return names


    def get_data(self, name):
        """
        returns the data corresponding to the name
        """
        for n, data in self.__content.items():
            if n.get_value() == name.get_value():
                return data
        return None


    def check_name(self, name):
        """
        It returns true if the name  is present in the content store and false it is not present
        """
        names = self.get_all_names()
        return name.get_value() in names


    def check_data(self, data):
        """
        It returns true if the data is present in the content store and false if is not present
        """
        return data in self.__content.values()


    def add(self, name, data):
        """
        adds (name,data) pair in the content store
        :param name: object of the Name class
        :param data: object of the Data class
        :return: True if successful, false if failure
        """
        try:
            if isinstance(name, Name) and isinstance(data, Data):
                self.__content[name] = data
                return True
            else:
                raise TypeError("Incorrect object type")
        except TypeError:
            print("Incorrect data or name format")
            return False


    def remove(self, name):
        """
        Removes the (name,data) pair from the content store
        :param name: object of the Name class
        :return:
        """
        try:
            self.__content.pop(name)
            return True
        except:
            print("Invalid name")
            return False


    def get_data_by_name(self, name):
        """
        Returns the contents of data for which the name(either prefix or whole ) is matching.
        :param name:  Name object.
        :return: List of Data object
        """

        if isinstance(name, Name):
            prefix = name.get_value()
        if isinstance(name, str):
            prefix = name
        res =[]
        for n, data in self.__content.items():
            pre=n.get_value()

            if pre.find(prefix) != -1:
                res.append(data)
        return res