import time

import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from classes import *

def get_courses_html():
    url = "https://reg.msu.edu/Courses/search.aspx"
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    subject = driver.find_element(By.NAME, "ctl00$MainContent$ddlSubjectCode")

    subject = Select(subject)
    subject.select_by_index(1)

    search_button = driver.find_element(By.NAME, "ctl00$MainContent$btnSubmit")
    search_button.click()

    while True:
        try:
            driver.find_element(By.ID, "MainContent_rptrSearchResults_divDescription_0")
            break
        except:
            time.sleep(1)


    return driver.find_element(By.ID, "MainContent_divSearchResults").text

def get_courses(html_source, placement_test_dict):
    courses_list = html_source.split("\n\n\n")
    for x in range(len(courses_list)):
        courses_list[x] = courses_list[x].split("\n")

    courses_list[0].pop(0)

    for course in courses_list:
        id, name = course[0].split("  ")

        semester = dict()
        credits = []
        reenroll_info = None
        prereqs = None
        coreqs = None
        recommended_background = None
        restrictions = None
        not_open_with_credit = None
        description = None
        semester_alias = None
        interdepartmental_with = None
        administered_by = None
        effective_dates = None

        extras = course[1:]
        for x in range(int(len(extras)/2)):
            descriptor = extras[x*2]
            data = extras[x*2+1]

            if descriptor == "Semester:":
                if data.lower() != "On Demand":
                    if ", " in data:
                        semester = data.split(", ")
                    else:
                        semester = [data]
                    for y in range(len(semester)):
                        semester[y] = semester[y].split(" ")[0]
                else:
                    semester = [data]

            elif descriptor == "Credits:":
                credits = data
                credits_dict = dict()
                if not "Variable" in credits:
                    credits = credits.split("  ")
                    for x in credits:
                        if "Total" in x:
                            credits_dict["Total"] = int(x.split(" ")[-1])
                        elif "Lecture" in x:
                            credits_dict["Lecture"] = int(x.split(" ")[-1])
                        elif "Lab" in x:
                            credits_dict["Lab"] = int(x.split(" ")[-1])
                else:
                    credits = credits.split(" ")
                    credits_dict["Max"] = int(credits[-1])
                    credits_dict["Min"] = int(credits[-3])

                if len(credits_dict) > 0: #I forgot if this is useless, test later
                    credits = credits_dict
                else:
                    credits = data

            elif descriptor == "Reenrollment Information:":
                if "maximum of " in data:
                    maximum_credits = data.split("maximum of ")
                    maximum_credits = maximum_credits[1][0]
                    maximum_credits = int(maximum_credits)
                    reenroll_info = [maximum_credits, data]
                else:
                    reenroll_info = [None, data]

            elif descriptor == "Prerequisite:":
                prereqs = Conditional(data, placement_test_dict, False)

            elif descriptor == "Corequisite:":
                coreqs = data
                coreqs = coreqs.split(" ")
                coreqs = " ".join(coreqs[:2])
                coreqs = Conditional(coreqs, placement_test_dict, False)

            elif descriptor == "Recommended Background:":
                recommended_background = data

            elif descriptor == "Restrictions:":
                restrictions = data

            elif descriptor == "Not open to students with credit in:":
                not_open_with_credit = Conditional(data, placement_test_dict, False)

            elif descriptor == "Description:":
                description = data

            elif descriptor == "Semester Alias:":
                semester_alias = data

            elif descriptor == "Interdepartmental With:":
                interdepartmental_with = data

            elif descriptor == "Administered By:":
                administered_by = data

            elif descriptor == "Effective Dates:":
                effective_dates = data

        index = courses_list.index(course)
        courses_list[index] = Course(id=id, name=name, semester=semester, credits=credits,
                                     reenrollment_info=reenroll_info, prerequisites=prereqs, corequisites=coreqs,
                                     recommended_background=recommended_background, restrictions=restrictions,
                                     not_open_with_credit=not_open_with_credit, description=description,
                                     alias=semester_alias, interdepartmental=interdepartmental_with,
                                     administered_by=administered_by, effective_dates=effective_dates)

    return courses_list

def get_majors_html():
    urls = [
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=114", # Agriculture and Natural Resources
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=115", # Arts and Humanities
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=116", # Arts and Letters
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=117", # Business and Management
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=118", # Communication Arts and Sciences
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=119", # Education
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=120", # Engineering !!!
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=121", # Human Medicine
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=122", # James Madison - Politics
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=123", # Law
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=124", # Lyman Briggs
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=125", # Music
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=126", # Natural Science
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=127", # Nursing
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=128", # Osteopathic Medicine
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=129", # Social Science
        "https://reg.msu.edu/AcademicPrograms/Text.aspx?Section=130", # Veterinary Medicine
    ]

    driver = selenium.webdriver.Chrome()
    for url in urls:
        driver.get(url)

        test = 0

placement_test_dict = {"Math":0, "French":0, "German":0, "Latin":0, "Spanish":0, "English":0, "Chinese":0, "Italian":0}
get_courses(get_courses_html(), placement_test_dict)
get_majors_html()