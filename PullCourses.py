class Course:
    def __init__(self, name, desc="", prerequisites=None, incompatible=None, semesters=None):
        if semesters is None:
            semesters = ["Fall", "Spring", "Summer"]
        if prerequisites is None:
            prerequisites = []
        if incompatible is None:
            incompatible = []
        self.name = name
        self.desc = desc
        self.prerequisites = prerequisites
        self.incompatible = incompatible
        self.semesters = semesters

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class Major:
    def __init__(self, name, desc, courses=None):
        if courses is None:
            courses = []
        self.name = name
        self.desc = desc
        self.courses = courses

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()