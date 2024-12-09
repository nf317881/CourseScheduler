class Course:
    def __init__(self, course_number, name, semester=None, credits=0, prerequisites=None, corequisites=None, restrictions=None, desc=""):
        if prerequisites is None:
            prerequisites = []
        if corequisites is None:
            corequisites = []
        if semester is None:
            semester = []

        self.prerequisites = prerequisites
        self.course_number = course_number
        self.name = name
        self.semester = semester
        self.credits = credits
        self.restrictions = restrictions
        self.desc = desc

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