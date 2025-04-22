import psycopg2 # pip install psycopg2-binary
import pandas as pd
from Webscraper.get_urls import get_course_urls
from get_df import create_df
# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="coursesDB",        # Your database name
    user="colin",            # Your PostgreSQL username
    password="barkley",      # Your PostgreSQL password
    host="localhost",        # Use 'db' if you're inside Docker
    port="5432"              # Default PostgreSQL port
)

# NU PATH Dictionary
nu_path = {

}

# Create a cursor to run queries
cursor = conn.cursor()

course_urls = get_course_urls()
columns = ['department_id', 'course_code', 'name', 'credits','description', 'corequisites', 'prerequisites', 'attributes']
df = pd.DataFrame(columns=columns)
for url in course_urls:
    new_df = create_df(url)
    df = pd.concat([df, new_df], ignore_index=True)

print("Columns", df.columns.tolist())


def populate_db():
    for index, row in df.iterrows():
        query = """
            SELECT department_id
            FROM departments
            WHERE prefix = %s
        """
        cursor.execute(query, (row['department_id'],))
        department_id = cursor.fetchone()  # get the department id

        if department_id is None:
            print(f"Department not found for prefix: {row['department_id']}")
            continue

        query = """
                INSERT INTO courses(department_id, course_code, name, description, credits)
                VALUES 
                    (%s, %s, %s, %s, %s)
            """

        try:
            cursor.execute(query, (department_id, row['course_code'], row['name'], row['description'], row['credits']))
            conn.commit()
        except Exception as e:
            print(e)

df.to_csv('courses.csv', index=False)
populate_db()

query = """
            SELECT *
            FROM courses
        """
cursor.execute(query)
results = cursor.fetchall()
print(results)