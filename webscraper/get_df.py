import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from get_urls import get_course_urls

def get_credits(data):
    extracted = []
    for s in data:
        match = re.search(r'(\d+)(?:-(\d+))?', s)
        if match:
            if match.group(2):
                extracted.append((int(match.group(1)), int(match.group(2))))  # range
            else:
                extracted.append(int(match.group(1)))  # single value
    return extracted




def clean_course_code(s):
    return s.replace('\xa0', ' ').strip()

def get_course_codes(element):
    course_codes = []
    a_elements = element.find_all("a")
    for i in range(0, len(a_elements), 2):
        course_codes.append(clean_course_code(a_elements[i].text))
    return course_codes


def get_attribute_list(attributes_text):
    attributes = attributes_text.replace('Attribute(s): ', '')
    attributes = attributes.split(',')
    clean_attributes = []
    for i in range(len(attributes)):
        attribute = attributes[i].replace(' NUpath ', '')
        if attribute[0] == ' ':
            attribute = attribute[1:]
        clean_attributes.append(attribute)
    return clean_attributes


columns = ['department_tag', 'course_code', 'name', 'credits','description', 'corequisites', 'prerequisites', 'attributes', 'department']

def create_df(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    df = pd.DataFrame(columns=columns)
    # get div that stores each individual course
    course_blocks = soup.find_all('div', class_ = 'courseblock')

    site_title = soup.find(id='site-title')
    wrap = site_title.find('div', class_ = 'wrap')
    parts = wrap.find('h1').text.strip().split(' ')
    department = parts[0]


    for block in course_blocks:
        p = block.find('p', class_='courseblocktitle noindent')
        strong = p.find('strong')
        text = strong.text.strip()
        parts = text.split('.')
        name = parts[1][2:]
        if 'Elective' in name:
            continue
        credit_list = get_credits(parts[2])
        if len(credit_list) != 1:
            continue

        credits = credit_list[0]
        course_info = clean_course_code(parts[0])
        parts = course_info.split(' ')


        department_tag = parts[0]
        course_code = parts[1]

        description = block.find('p', class_='cb_desc').text.strip()
        elements = soup.find_all('p', class_='courseblockextra noindent')

        # Get additional elements
        prequisites = None
        corequisites = None
        attributes = None

        for p in elements:
            if not p is None:
                text = p.find('strong').text.strip()
                if text == 'Prerequisite(s):':
                    prequisites = get_course_codes(p)
                elif text == 'Corequisite(s):':
                    corequisites = get_course_codes(p)
                else:
                    attributes = p.text.strip()
                    attributes = get_attribute_list(attributes)


        if None in [department_tag, course_code, name, credits, description, corequisites, prequisites, attributes]:
           continue
        df.loc[len(df)] = [department_tag, course_code, name, credits, description, corequisites, prequisites, attributes, department]
    return df


create_df("https://catalog.northeastern.edu/course-descriptions/arch/")


