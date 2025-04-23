from bs4 import BeautifulSoup
import requests


# URL for all course descriptions
url = "https://catalog.northeastern.edu/course-descriptions/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

BASE_URL = "https://catalog.northeastern.edu"

def get_course_urls():
    urls = []
    div = soup.find('div', id="atozindex")
    list_elements = div.find_all('li')
    for li in list_elements:
        a = li.find("a")
        if a is None:
            continue
        urls.append(BASE_URL + a["href"])
    return urls


