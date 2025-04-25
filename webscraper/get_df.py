import pandas as pd
import requests
import re
from bs4 import BeautifulSoup, NavigableString
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


def get_prerequisites(parts):
    prerequisites = []
    group = 1

    for i in range(1, len(parts)):

        if 'with' in parts[i]:

            split = parts[i].split('or ')

            if len(split) == 1:
                if ');' in split[0]:
                    group += 1
                continue

            if len(split) == 2:
                if split[1] == ' ':
                    continue
                tokens = split[1][1:].split(' ')
                if len(tokens) == 1 or not tokens[1].isdigit():
                    continue

                course_code = tokens[0] + ' ' + tokens[1]
                prerequisites.append((course_code, group))

                if ');' in tokens:

                    group += 1
        elif '(' in parts[i] or 'or' in parts[i]:
            continue
        elif ')' in parts[i] or 'and' in parts[i]:
            group += 1
        else:
            course_code = clean_course_code(parts[i])
            prerequisites.append((course_code, group))

    return prerequisites



columns = ['department_tag',
           'course_code',
           'name',
           'credits',
           'description',
           'corequisites',
           'prerequisites',
           'attributes',
           'department',
           'group_numbers']

def create_df(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    df = pd.DataFrame(columns=columns)
    # get div that stores each individual course
    course_blocks = soup.find_all('div', class_ = 'courseblock')

    site_title = soup.find(id='site-title')
    wrap = site_title.find('div', class_ = 'wrap')
    parts = wrap.find('h1').text.strip().split(' ')

    department = ' '.join(parts[:-1])




    for block in course_blocks:

        prerequisites = []
        corequisites = []
        attributes = []

        # Get Type of Course
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
        elements = block.find_all('p', class_='courseblockextra noindent')

        # Get additional elements
        for p in elements:
            if not p is None:

                strong = p.find('strong')
                if strong is None:
                    continue
                text = strong.text.strip()
                if text == 'Prerequisite(s):':

                    course_codes = get_course_codes(p)
                    parts = []
                    for content in p.contents:
                        if isinstance(content, NavigableString):
                            parts.append(str(content))
                        else:
                            parts.append(content.get_text())

                    prerequisites = get_prerequisites(parts)


                elif text == 'Corequisite(s):':
                    corequisites = get_course_codes(p)
                else:
                    attributes = p.text.strip()
                    attributes = get_attribute_list(attributes)

        if None in [department_tag, course_code, name, credits, description]:
           continue
        group_numbers = []
        course_codes = []
        for prereq_tuple in prerequisites:
            course_codes.append(prereq_tuple[0])
            group_numbers.append(prereq_tuple[1])
        df.loc[len(df)] = [department_tag,
                           course_code,
                           name,
                           credits,
                           description,
                           corequisites,
                           course_codes,
                           attributes,
                           department,
                           group_numbers]

    return df


df = create_df('https://catalog.northeastern.edu/course-descriptions/cs/')


