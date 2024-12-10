
class Course:
    def __init__(self, id, name, semester, credits, reenrollment_info=None, prerequisites=None, corequisites=None, recommended_background=None,
                 restrictions=None, not_open_with_credit=None, description=None, alias=None, interdepartmental=None,
                 administered_by=None, effective_dates=None):

        if not_open_with_credit is None:
            not_open_with_credit = []
        if corequisites is None:
            corequisites = []
        if prerequisites is None:
            prerequisites = []

        self.id = id
        self.name = name
        self.semester = semester
        self.credits = credits
        self.reenrollment_info = reenrollment_info
        self.prerequisites = prerequisites
        self.corequisites = corequisites
        self.recommended_background = recommended_background
        self.restrictions = restrictions
        self.not_open_with_credit = not_open_with_credit
        self.description = description
        self.alias = alias
        self.interdepartmental = interdepartmental
        self.administered_by = administered_by
        self.effective_dates = effective_dates

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



class Conditional:
    def __init__(self, str_cond):
        opening_parenthesis = 0
        for char in str_cond:
            if char == '(':
                opening_parenthesis += 1
            elif char == ')':
                opening_parenthesis -= 1

            index = str_cond.index(char)
            if char == 'a' and str_cond[index + 1] == 'n' and str_cond[index + 2] == 'd' and \
                opening_parenthesis == 0:

                self.split_type = "and"
                self.split = index

            if char == 'o' and str_cond[index + 1] == 'r' and opening_parenthesis == 0:
                self.split_type = "or"
                self.split = []
                self.split.append(index)


        self.conds = []
        if self.split_type == "and":
            if str_cond[self.split+4:] != "Concurrently":
                cond_1 = str_cond[:self.split-1]
                cond_2 = str_cond[self.split+4:]

                if "or" in cond_1 or "and" in cond_1:
                    if "(" in cond_1:
                        cond_1 = Conditional(cond_1[1:-1])
                    else:
                        cond_1 = Conditional(cond_1)

                if "or" in cond_2 or "and" in cond_2:
                    if "(" in cond_2:
                        cond_2 = Conditional(cond_2[1:-1])
                    else:
                        cond_2 = Conditional(cond_2)

                self.conds.append(cond_1)
                self.conds.append(cond_2)
            else:
                self.split_type = "concurrent"
                self.conds = str_cond[:self.split-1]

        elif self.split_type == "or":
            for x in range(len(self.split)):
                if x == 0:
                    self.conds.append(str_cond[:self.split[x]-1])
                elif x == len(self.split)-1:
                    self.conds.append(str_cond[self.split[x]+3:])
                else:
                    self.conds.append(str_cond[self.split[x-1]+3:self.split[x]-1])

        else:
            self.split_type = "none"
            self.conds = str_cond

    def check_if_courses_in(self, course_id_list_previous, course_id_list_current):
        if self.split_type == "none":
            return_value = self.conds in course_id_list_previous
        elif self.split_type == "and":
            return_value = self.conds[0].check_if_courses_in(course_id_list_previous) and self.conds[1].check_if_courses_in(course_id_list_previous)
        elif self.split_type == "or":
            return_value = False
            for x in self.conds:
                if x.check_if_courses_in(course_id_list_previous):
                    return_value = True
        elif self.split_type == "concurrent":
            return_value = self.conds in course_id_list_current or self.conds in course_id_list_previous

        return return_value