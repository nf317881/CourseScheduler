import time

import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import classes

def get_html():
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

def get_courses(html_source):
    courses_list = html_source.split("\n\n\n")
    for x in range(len(courses_list)):
        courses_list[x] = courses_list[x].split("\n")

    courses_list[0].pop(0)

    for course in courses_list:
        id, name = course[0].split("  ")

        semester = course[2]
        if ", " in semester:
            semester = semester.split(", ")
        else:
            semester = [semester]
        for x in range(len(semester)):
            semester[x] = semester[x].split(" ")[0]

        credits = course[4]
        credits = credits.split("  ")[0]
        credits = credits.split(" ")[-1]
        credits = int(credits)





get_courses(get_html())