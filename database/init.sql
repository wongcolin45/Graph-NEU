


-- Drop dependent tables first
DROP TABLE IF EXISTS course_prerequisites, corequisites, courses, departments, nu_path CASCADE;

-- Drop enum type
DROP TYPE IF EXISTS corequisite_type;

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    prefix TEXT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    department_id INT NULL, -- allow to be null
    course_code INT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    credits INT DEFAULT 4,
    UNIQUE(department_id, course_code),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TYPE corequisite_type AS ENUM ('lecture', 'lab', 'seminar');

CREATE TABLE corequisites (
    corequisite_id SERIAL PRIMARY KEY,
    course_id INT NULL,
    course_code INT NOT NULL,
    type corequisite_type NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    credits INT DEFAULT 2,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE course_prerequisites(
    course_id INT NOT NULL,
    prerequisite_id INT NOT NULL,
    PRIMARY KEY(course_id, prerequisite_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_id) REFERENCES courses(course_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE nu_path (
    name TEXT PRIMARY KEY
);


