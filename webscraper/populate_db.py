import psycopg2 # pip install psycopg2-binary
import pandas as pd
import ast
from get_urls import get_course_urls
from get_df import create_df
import numpy as np
# Connect to your PostgresSQL db
conn = psycopg2.connect(
    dbname="coursesDB",
    user="colin",
    password="barkley",
    host="localhost",
    port="5432"
)


# Create a cursor to run queries
cursor = conn.cursor()

# Get Course ID
def get_course_id(department_tag, course_code):
    try:
        query = """
                SELECT c.course_id
                FROM courses c
                JOIN departments d ON d.department_id = c.department_id
                WHERE d.prefix = %s AND c.course_code = %s
                """
        cursor.execute(query, (department_tag, course_code))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]
    except Exception as e:
        print("GET COURSE ID ERROR: ",e)
        conn.rollback()
        return None

# Get Department ID
def get_department_id(department_tag):
    try:
        query = """
                    SELECT department_id
                    FROM departments
                    WHERE prefix = %s
                """
        cursor.execute(query, (department_tag,))
        department_id = cursor.fetchone()
        return department_id
    except Exception as e:
        #print("GET DEPARTMENT ID ERROR: ",e)
        # print(e)
        conn.rollback()
        return None

# Add New Department
def add_department(department_tag, department):
    try:
        query = """
                    INSERT INTO departments (prefix, name)
                    VALUES (%s, %s)
                """
        cursor.execute(query, (department_tag, department))
    except Exception as e:
        # print("ADD DEPARTMENT ERROR: ",e)
        print(e)
        conn.rollback()

# Add Course Attributes
def insert_attributes(course_id, attributes):
    for attribute in attributes:
        try:
            # Get the attribute id
            query = """
                    SELECT attribute_id
                    FROM attributes
                    WHERE tag = %s
                    """
            cursor.execute(query, (attribute,))
            attribute_id = cursor.fetchone()
            if attribute_id is None:
                print(f"Attribute tag not found: {attribute}")
                continue
            attribute_id = attribute_id[0]
            # No
            query = """
                    INSERT INTO course_attributes (course_id, attribute_id)
                    VALUES (%s, %s)
                    """
            cursor.execute(query, (course_id, attribute_id))
        except Exception as e:
            print('inserting attributes failed')
            conn.rollback()

    conn.commit()

# Add Course Prerequisites
def insert_prerequisites(df):
    for index, row in df.iterrows():
        course_id = get_course_id(row['department_tag'], row['course_code'])

        if course_id is None:
            #print(f'Cant find {row['department_tag']} - {row['course_code']}')
            continue


        for idx, prereq in enumerate(row['prerequisites']):
            preq = prereq
            group = row['group_numbers'][idx]
            parts = preq.split(' ')

            preq_id = get_course_id(parts[0], parts[1])

            if not preq_id:
                continue

            try:
                query = """
                        INSERT INTO course_prerequisites(course_id, prerequisite_id, group_number)
                        VALUES (%s, %s, %s)   
                        """
                cursor.execute(query, (course_id, preq_id, group))
                conn.commit()
            except Exception as e:
                #print(f'INSERT PREREQUISITES ERROR: ', e)
                error = e
                print(e)
                conn.rollback()


def convert_str_list(df):
    columns_to_convert = ['prerequisites', 'corequisites', 'attributes', 'group_numbers']
    for col in columns_to_convert:
        df[col] = df[col].apply(
            lambda x: [] if isinstance(x, float) and pd.isna(x)
            else list(x) if isinstance(x, np.ndarray)
            else ast.literal_eval(x) if isinstance(x, str)
            else x
        )

def insert_courses(df):
    for index, row in df.iterrows():
        # Get the department id
        department_id = get_department_id(row['department_tag'])
        #print(department_id)
        if department_id is None:
            continue
        if row['credits'] == 0:
            continue
        # Attempt to insert into course tables
        try:
            query = """
                    INSERT INTO courses(department_id, course_code, name, description, credits)
                    VALUES 
                        (%s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (department_id, row['course_code'], row['name'], row['description'], row['credits']))
            conn.commit()
            course_id = get_course_id(row['department_tag'], row['course_code'])
            insert_attributes(course_id, row['attributes'])
        except Exception as e:
            print('inserting course failed '+str(e))
            conn.rollback()




# Main Script Here:

urls = get_course_urls()

# create csv
# df = pd.DataFrame()
#
# for url in urls:
#     new_df = create_df(url)
#     df = pd.concat([df, new_df], ignore_index=True)
#
#
# df.to_csv('courses.csv', index=False)




# Populate DB
df = pd.read_csv('courses.csv')
convert_str_list(df)
insert_courses(df)
prereqs = df['prerequisites'][0]
insert_prerequisites(df)
