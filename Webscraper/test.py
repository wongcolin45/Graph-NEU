import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import psycopg2 # pip install psycopg2-binary
import pandas as pd
import ast

from get_urls import get_course_urls
from get_df import create_df






course_urls = get_course_urls()

# columns in our df
columns = ['department_tag', 'course_code', 'name', 'credits','description', 'corequisites', 'prerequisites', 'attributes', 'department']

df = pd.DataFrame(columns=columns)

for url in course_urls:
    department_df = create_df(url)
    df = pd.concat([df, department_df], ignore_index=True)



