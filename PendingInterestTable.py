from Name import Name
from Face import Face

class PendingInterestTable:
    """
    Defines the pending interest table (PIT) in a node

    eg:-
    from PendingInterestTable import PendingInterestTable
    from Name import Name
    from Face import Face

    pit = PendingInterestTable()
    name1 = Name("name1")
    name2 = Name("name2")
    face1 = Face("face1")
    face2 = Face("face2")
    pit.add(name1,face1)
    print(pit)
    print(pit.get())
    print(pit.get_value())
    print(pit.get_all_interests())
    print(pit.get_faces(name1))

    pit.add(name1,face2)
    print(pit.get())
    print(pit.get_all_prefixes())
    print(pit.get_faces(name1))
    """

    def __init__(self):
        self.__pending_interest = {}


    def __str__(self):
        return str(self.get())


    def get(self):
        """
        returns the list of (name_prefix, requested_faces) as a dictionary
        """
        pending_interests = {}

        for name_prefix,requesting_faces in self.__pending_interest.items():
            faces = []
            for face in requesting_faces:
                if isinstance(face, Face):
                    faces.append(face.get_value())
            pending_interests[name_prefix.get_value()] = faces

        return pending_interests

    def get_value(self):
        """
        returns the list of names prefixes in the table
        """
        return self.get_all_prefixes()


    def get_all_prefixes(self):
        """
        returns the list of name prefixes in the table
        """
        name_prefixes = []
        for prefix,faces in self.__pending_interest.items():
            name_prefixes.append(prefix.get_value())
        return name_prefixes


    def get_all_interests(self):
        return self.get_all_prefixes()

    def get_faces(self, name_prefix):
        """
        returns the list of requesting faces in the table for a given name prefix
        :param name_prefix: Object of the Name class
        """
        if isinstance(name_prefix, Name):
            name = name_prefix.get_value()
        else:
            name = name_prefix
        interests = self.get()
        if name in interests:
            return interests[name]
        else:
            return None


    def check_name_prefix(self, name_prefix):
        """
        checks whether any face has requested data for the given name_prefix
        If the name_prefix is present then it will return true or else it will return false
        """
        if isinstance(name_prefix, Name):
            name_pre = name_prefix.get_value()
        if isinstance(name_prefix, str):
            name_pre = name_prefix
        return name_pre in self.get_all_interests()


    def add(self, name_prefix, requesting_faces):
        """
        adds the (name_prefix, requesting_face) in the table. Each prefix can have multiple requesting_faces
        :param name_prefix: It is the object of the Name class
        :param requesting_faces: It is the object of the Face class
        :return: True if successful and False if failure
        """
        try:
            if not (isinstance(name_prefix, Name)):
                raise TypeError("Incorrect name_prefix. Pass the name class object")
            if requesting_faces is list:
                for face in requesting_faces:
                    if not (isinstance(face, Face)):
                        raise TypeError("Incorrect face. Pass the face class object")
            else:
                if not (isinstance(requesting_faces, Face)):
                    raise TypeError("Incorrect name_prefix. Pass the name class object")
            faces = []
            if name_prefix in self.__pending_interest:
                for face in self.__pending_interest[name_prefix]:
                    faces.append(face)
            faces.append(requesting_faces)
            self.__pending_interest[name_prefix] = faces
            return True
        except TypeError:
            print("incorrect format")
            return False



    def remove(self, name_prefix):
        """
        Removes the name_prefix,faces from the table
        :param name_prefix: It is the name object
        :return:
        """
        if isinstance(name_prefix, Name):
            name = name_prefix.get_value()

        target = None
        for name_pre, faces in self.__pending_interest.items():
            if name_prefix == name_pre:
                target = name_prefix
                break
        if target is not None:
            del self.__pending_interest[name_prefix]
            return True
        return False