
class Course:
    def __init__(self, id, name, semester, credits, reenrollment_info=None, prerequisites=None, corequisites=None, recommended_background=None,
                 restrictions=None, not_open_with_credit=None, description=None, alias=None, interdepartmental=None,
                 administered_by=None, effective_dates=None):

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

    def check_if_allowed(self, previous_courses, concurrent_courses):
        allowed = True

        if self.prerequisites is not None:
            allowed = self.prerequisites.check_if_courses_in(previous_courses)

        if self.corequisites is not None:
            allowed = self.corequisites.check_if_courses_in(previous_courses)

        if self.restrictions is not None:
            allowed = not self.restrictions.check_if_courses_in(previous_courses)

        return allowed


class Major:
    def __init__(self, name, desc, courses=None):
        if courses is None:
            courses = []
        self.name = name
        self.desc = desc
        self.courses = courses

    def check_completed(self, course_list):
        completed = True
        courses_not_met = []
        for course in self.courses:
            if not course in course_list:
                completed = False
                courses_not_met.append(course)

        return [completed, courses_not_met]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()



class Conditional:
    def __init__(self, str_cond, placement_test_dict, tier_1_writing_requirement):
        self.str_cond = str_cond
        if str_cond == "(CSS 232) Completion of Tier I writing requirement.":
            str_cond = "CSS 232 and Completion of Tier I writing requirement"

        if type(tier_1_writing_requirement) is not bool:
            tier_1_writing_requirement = False
        translation_table = str.maketrans(
            {"{": "(", "}": ")", ".":""})
        self.str_cond = str_cond.translate(translation_table)
        self.str_cond.replace("Completion of Tier I Writing Requirement", str(tier_1_writing_requirement))

        self.math_placement_test_score = placement_test_dict["Math"]

        if self.malicious_check():  # str_cond is from the web and we eval later
                                    # if str_cond without (), num, and spaces is not alpha end program
            raise ValueError("Invalid condition string:", str_cond)

        spaces = []
        all_separators = []
        for index, char in enumerate(self.str_cond):
            if char == " ":
                spaces.append(index)
                all_separators.append(index)
            elif char == "(":
                all_separators.append(index)
            elif char == ")":
                all_separators.append(index)

        courses = []
        if len(all_separators) > 1:
            for index, x in enumerate(spaces):
                all_sep_index = all_separators.index(x)
                if self.str_cond[x + 1].isdigit():
                    if all_sep_index != 0:
                        start = all_separators[all_sep_index - 1] + 1
                    else:
                        start = 0

                    if not all_sep_index == len(all_separators) - 1:
                        end = all_separators[all_sep_index + 1]
                    else:
                        end = len(all_separators) - 1
                    # 0 is course name, 1 is starting char in str_cond, 2 is end, 3 is if the course should be considered
                    # as concurrent
                    courses.append([self.str_cond[start:end], start, end, False])
        else:
            courses.append([self.str_cond, 0, len(self.str_cond)-1, False]) #this is for conditions of only 1 course

        # if a course is concurrently allowed, create a new class with concurrently allowed
        # this works well because the str_cond is modified to be .eval() later
        while "concurrently" in self.str_cond:
            start = self.str_cond.index("concurrently")
            end = start + 12
            for index, course in enumerate(courses):
                if len(courses) > index + 1 and courses[index + 1][1] > end:
                    courses.append([course[0], start, end, True])
                    break
                elif index + 1 == len(courses):
                    courses.append([course[0], start, end, True])
                    break
            self.str_cond = self.str_cond[:start] + "_handled_it_" + self.str_cond[end:]

        self.courses = courses

    def check_if_courses_in(self, course_id_list_previous, course_id_list_current):
        cond_copy = self.str_cond

        # the website has inconsistent capitalization
        if " or designated score on Mathematics Placement test" in cond_copy or \
            " or Designated score on Mathematics Placement test" in cond_copy:

            if self.math_placement_test_score >= 15:
                course_id_list_previous.append("MTH 101", "MTH 102", "MTH 103A", "MTH 103B", "MTH 103", "MTH 114",
                                               "MTH 116", "LB 117")

        elif "Designated score on Mathematics Placement test" == cond_copy:
            if self.courses[0][0] == "MTH 103":
                return self.math_placement_test_score >= 10
            if self.courses[0][0] == "MTH 116":
                return self.math_placement_test_score >= 12

        # we modify the condition string, this makes sure it is edited from back to front
        self.courses.sort(key=lambda course: course[1], reverse=True)
        for course in self.courses:
            concurrent_allowed = course[3]

            if not concurrent_allowed:
                course_bool = course[0] in course_id_list_previous
            else:
                course_bool = course[0] in course_id_list_current or course[0] in course_id_list_previous

            # change courses, ie CSE 231, to True or False
            cond_copy = cond_copy[:course[1]] + str(course_bool) + cond_copy[course[2]:]

        return eval(cond_copy)

    def malicious_check(self):
        # if someone wants to inject code by the official MSU course catalog the code will probably have . or :
        # if it does end the program because the course catalog is probably compromised, as would've been this program
        cond_copy = self.str_cond
        translation_table = str.maketrans({"(":"", ")":"", "0":"", "1":"", "2":"", "3":"", "4":"", "5":"", "6":"",
                                           "7":"", "8":"", "9":"", " ":""})
        cond_copy = cond_copy.translate(translation_table)
        return not cond_copy.isalpha()

    def __str__(self):
        return self.str_cond

    def __repr__(self):
        return self.__str__()

    def get_cond_str(self):
        return self.__str__()

    def new_math_placement_test_score(self, number):
        if type(number) == int:
            self.math_placement_test_score = number
        else:
            # math placement test scores are not fractional or otherwise outside Z+
            raise ValueError("Number must be an integer")


class Semester():
    def __init__(self, courses=None, year=1900, season="Fall"):
        if courses is None or type(courses) is not list or type(courses[0]) is not Course:
            courses = []

        if type(year) is not int:
            year = 1900

        if type(season) is not str:
            season="Fall"

        self.courses = courses
        self.year = year
        self.season = season

        if season == "Fall":
            self.truncated_season = "FA"
        elif season == "Spring":
            self.truncated_season = "SP"
        elif season == "Summer":
            self.truncated_season = "SU"

    def __str__(self):
        return f"{self.truncated_season}{str(self.year)[2:]}"

    def __repr__(self):
        return self.__str__()



class Schedule():
    def __init__(self, name, semesters=None, majors=None):
        if semesters is None or type(semesters) is not list or type(semesters[0]) is not Semester:
            semesters = []
        if majors is None or type(majors) is not list or type(majors[0]) is not Major:
            majors = []

        self.semesters = semesters
        self.majors = majors
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def check_majors_completion(self):
        satisfied_courses = []
        unsatisfied_courses = []
        for semester in self.semesters:
            for course in semester.courses:
                if course.check_if_allowed(satisfied_courses, semester.courses):
                    satisfied_courses.append(course)
                else:
                    unsatisfied_courses.append(course)

        satisfied_majors = []
        unsatisfied_majors = []
        for major in self.majors:
            if major.check_completed(satisfied_courses):
                satisfied_majors.append(major)
            else:
                unsatisfied_majors.append(major)

        return [satisfied_courses, unsatisfied_courses, satisfied_majors, unsatisfied_majors]