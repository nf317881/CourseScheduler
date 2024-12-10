import time

import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from classes import *

def get_html():
    url = "https://reg.msu.edu/Courses/search.aspx"
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    subject = driver.find_element(By.NAME, "ctl00$MainContent$ddlSubjectCode")

    subject = Select(subject)
    subject.select_by_index(2)

    search_button = driver.find_element(By.NAME, "ctl00$MainContent$btnSubmit")
    search_button.click()

    while True:
        try:
            driver.find_element(By.ID, "MainContent_rptrSearchResults_divDescription_0")
            break
        except:
            time.sleep(1)


    return driver.find_element(By.ID, "MainContent_divSearchResults").text

def get_courses(html_source):
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
                if ", " in data:
                    semester = data.split(", ")
                else:
                    semester = [data]
                for y in range(len(semester)):
                    semester[y] = semester[y].split(" ")[0]

            elif descriptor == "Credits:":
                credits = data
                credits = credits.split("  ")
                credits_dict = dict()
                for x in credits:
                    if "Total" in x:
                        credits_dict["Total"] = int(x.split(" ")[-1])
                    elif "Lecture" in x:
                        credits_dict["Lecture"] = int(x.split(" ")[-1])
                    elif "Lab" in x:
                        credits_dict["Lab"] = int(x.split(" ")[-1])
                if len(credits_dict) > 0:
                    credits = credits_dict
                else:
                    credits = data

            elif descriptor == "Reenrollment Information:":
                reenroll_info = data

            elif descriptor == "Prerequisite:":
                test = 0

            elif descriptor == "Corequisite:":
                coreqs = data
                coreqs = coreqs.split(" ")
                coreqs = " ".join(coreqs[:2])

            elif descriptor == "Recommended Background:":
                recommended_background = data

            elif descriptor == "Restrictions:":
                restrictions = data

            elif descriptor == "Not open to students with credit in:":
                not_open_with_credit = data

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



get_courses(get_html())