# -*- coding: utf-8 -*-
"""
This file contains the data models and database interaction logic for the
university management system.
"""
import sqlite3
import os

DB_FILE = "university.db"

class University:
    """
    A controller class to manage all database interactions for the university system.
    """
    def __init__(self, db_path):
        """Initializes the University and connects to the database."""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        """Creates the necessary database tables if they don't exist."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            role TEXT NOT NULL,
            university_id TEXT UNIQUE NOT NULL
        )''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            professor_id INTEGER,
            FOREIGN KEY (professor_id) REFERENCES persons (id)
        )''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            course_id INTEGER,
            student_id INTEGER,
            PRIMARY KEY (course_id, student_id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            FOREIGN KEY (student_id) REFERENCES persons (id)
        )''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            student_id INTEGER,
            course_id INTEGER,
            grade TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES persons (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )''')
        self.conn.commit()

    def add_student(self, name, age, student_id):
        """Adds a new student to the database."""
        try:
            self.cursor.execute("INSERT INTO persons (name, age, role, university_id) VALUES (?, ?, 'student', ?)",
                                (name, age, student_id))
            self.conn.commit()
            return f"Student '{name}' added successfully."
        except sqlite3.IntegrityError:
            return f"Error: Student with ID '{student_id}' already exists."

    def add_professor(self, name, age, employee_id):
        """Adds a new professor to the database."""
        try:
            self.cursor.execute("INSERT INTO persons (name, age, role, university_id) VALUES (?, ?, 'professor', ?)",
                                (name, age, employee_id))
            self.conn.commit()
            return f"Professor '{name}' added successfully."
        except sqlite3.IntegrityError:
            return f"Error: Professor with ID '{employee_id}' already exists."

    def add_course(self, name, code):
        """Adds a new course to the database."""
        try:
            self.cursor.execute("INSERT INTO courses (name, code) VALUES (?, ?)", (name, code))
            self.conn.commit()
            return f"Course '{name}' added successfully."
        except sqlite3.IntegrityError:
            return f"Error: Course with code '{code}' already exists."

    def assign_professor_to_course(self, professor_identifier, course_code):
        """Assigns a professor to a course.
        professor_identifier can be the university_id (e.g. 'P54321') or the professor name.
        """
        # Try to find professor by university_id first, then by name (case-insensitive)
        self.cursor.execute(
            "SELECT id, name, university_id FROM persons WHERE university_id = ? AND role = 'professor'",
            (professor_identifier,)
        )
        prof = self.cursor.fetchone()
        if not prof:
            self.cursor.execute(
                "SELECT id, name, university_id FROM persons WHERE lower(name) = lower(?) AND role = 'professor'",
                (professor_identifier,)
            )
            prof = self.cursor.fetchone()

        # Find course by code (case-insensitive)
        self.cursor.execute("SELECT id, code FROM courses WHERE lower(code) = lower(?)", (course_code,))
        course = self.cursor.fetchone()

        if not prof:
            return f"Error: Professor '{professor_identifier}' not found."
        if not course:
            return f"Error: Course with code '{course_code}' not found."

        try:
            self.cursor.execute("UPDATE courses SET professor_id = ? WHERE id = ?", (prof[0], course[0]))
            self.conn.commit()
            return f"Professor '{prof[1]}' (ID: {prof[2]}) assigned to course '{course[1]}'."
        except Exception as e:
            return f"Error: Failed to assign professor: {e}"

    def enroll_student_in_course(self, student_id, course_code):
        """Enrolls a student in a course."""
        self.cursor.execute("SELECT id FROM persons WHERE university_id = ? AND role = 'student'", (student_id,))
        student = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM courses WHERE code = ?", (course_code,))
        course = self.cursor.fetchone()
        if student and course:
            try:
                self.cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student[0], course[0]))
                self.conn.commit()
                return f"Student '{student_id}' enrolled in course '{course_code}'."
            except sqlite3.IntegrityError:
                return f"Error: Student '{student_id}' is already enrolled in '{course_code}'."
        return "Error: Could not find student or course."

    def assign_grade(self, student_id, course_code, grade):
        """Assigns a grade to a student for a specific course."""
        self.cursor.execute("SELECT id FROM persons WHERE university_id = ? AND role = 'student'", (student_id,))
        student = self.cursor.fetchone()
        self.cursor.execute("SELECT id FROM courses WHERE code = ?", (course_code,))
        course = self.cursor.fetchone()
        if student and course:
            self.cursor.execute("SELECT * FROM enrollments WHERE student_id = ? AND course_id = ?", (student[0], course[0]))
            if self.cursor.fetchone():
                self.cursor.execute("INSERT OR REPLACE INTO grades (student_id, course_id, grade) VALUES (?, ?, ?)", (student[0], course[0], grade))
                self.conn.commit()
                return f"Grade '{grade}' assigned to student '{student_id}' for course '{course_code}'."
            return f"Error: Student '{student_id}' is not enrolled in course '{course_code}'."
        return "Error: Could not find student or course."

    def get_people(self, role):
        """Fetches all people of a specific role (student or professor)."""
        self.cursor.execute("SELECT name, age, university_id FROM persons WHERE role = ?", (role,))
        return self.cursor.fetchall()

    def get_courses(self):
        """Fetches all courses."""
        query = """
        SELECT c.name, c.code, p.name from courses c
        LEFT JOIN persons p ON c.professor_id = p.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_course_summary(self, course_code):
        """Fetches summary for a specific course."""
        query = """
        SELECT p.name, p.university_id FROM persons p
        JOIN enrollments e ON p.id = e.student_id
        JOIN courses c ON e.course_id = c.id
        WHERE c.code = ?
        """
        self.cursor.execute(query, (course_code,))
        return self.cursor.fetchall()

    def get_student_grades(self, student_id):
        """Fetches all grades for a specific student."""
        query = """
        SELECT c.name, c.code, g.grade FROM grades g
        JOIN persons p ON g.student_id = p.id
        JOIN courses c ON g.course_id = c.id
        WHERE p.university_id = ?
        """
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchall()
        
    def get_all_table_names(self):
        """Fetches all table names from the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    def get_table_contents(self, table_name):
        """Fetches all contents for a specific table."""
        self.cursor.execute(f"SELECT * FROM {table_name}")
        contents = self.cursor.fetchall()
        # Get column headers
        headers = [description[0] for description in self.cursor.description]
        return headers, contents

    def close(self):
        """Closes the database connection."""
        self.conn.close()
        
def initialize_database():
    """Wipes and sets up the database with sample data."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    university = University(DB_FILE)
    # sample data to get started
    print("--- Initializing Database with Sample Data ---")
    # Add 10 students
    university.add_student("Alice", 20, "S12345")
    university.add_student("Bob", 22, "S67890")
    university.add_student("Charlie", 21, "S11223")
    university.add_student("David", 23, "S44556")
    university.add_student("Eva", 19, "S77889")
    university.add_student("Frank", 24, "S33445")
    university.add_student("Grace", 20, "S55667")
    university.add_student("Hannah", 22, "S88990")
    university.add_student("Ian", 21, "S99001")
    university.add_student("Julia", 23, "S10203")

    # Add 10 professors
    university.add_professor("Dr. Smith", 45, "P54321")
    university.add_professor("Dr. Jones", 52, "P98765")
    university.add_professor("Dr. Brown", 48, "P11223")
    university.add_professor("Dr. Taylor", 50, "P33445")
    university.add_professor("Dr. Wilson", 55, "P55667")
    university.add_professor("Dr. Lee", 47, "P77889")
    university.add_professor("Dr. Clark", 53, "P99001")
    university.add_professor("Dr. Lewis", 49, "P10203")
    university.add_professor("Dr. Walker", 51, "P20304")
    university.add_professor("Dr. Hall", 46, "P30405")

    # Add 10 courses
    university.add_course("Introduction to Python", "CS101")
    university.add_course("Advanced Algorithms", "CS301")
    university.add_course("Database Systems", "CS201")
    university.add_course("Operating Systems", "CS202")
    university.add_course("Computer Networks", "CS203")
    university.add_course("Software Engineering", "CS204")
    university.add_course("Artificial Intelligence", "CS205")
    university.add_course("Machine Learning", "CS206")
    university.add_course("Data Structures", "CS102")
    university.add_course("Web Development", "CS207")

    # Assign professors to courses
    university.assign_professor_to_course("P54321", "CS101")
    university.assign_professor_to_course("P98765", "CS301")
    university.assign_professor_to_course("P11223", "CS201")
    university.assign_professor_to_course("P33445", "CS202")
    university.assign_professor_to_course("P55667", "CS203")
    university.assign_professor_to_course("P77889", "CS204")
    university.assign_professor_to_course("P99001", "CS205")
    university.assign_professor_to_course("P10203", "CS206")
    university.assign_professor_to_course("P20304", "CS102")
    university.assign_professor_to_course("P30405", "CS207")

    # Enroll students in courses (each student in 2-3 courses)
    university.enroll_student_in_course("S12345", "CS101")
    university.enroll_student_in_course("S12345", "CS201")
    university.enroll_student_in_course("S67890", "CS101")
    university.enroll_student_in_course("S67890", "CS301")
    university.enroll_student_in_course("S11223", "CS301")
    university.enroll_student_in_course("S11223", "CS202")
    university.enroll_student_in_course("S44556", "CS203")
    university.enroll_student_in_course("S44556", "CS204")
    university.enroll_student_in_course("S77889", "CS205")
    university.enroll_student_in_course("S77889", "CS206")
    university.enroll_student_in_course("S33445", "CS102")
    university.enroll_student_in_course("S33445", "CS207")
    university.enroll_student_in_course("S55667", "CS201")
    university.enroll_student_in_course("S55667", "CS202")
    university.enroll_student_in_course("S88990", "CS203")
    university.enroll_student_in_course("S88990", "CS204")
    university.enroll_student_in_course("S99001", "CS205")
    university.enroll_student_in_course("S99001", "CS206")
    university.enroll_student_in_course("S10203", "CS102")
    university.enroll_student_in_course("S10203", "CS207")

    # Assign grades to students for their courses
    university.assign_grade("S12345", "CS101", "A")
    university.assign_grade("S12345", "CS201", "B+")
    university.assign_grade("S67890", "CS101", "B")
    university.assign_grade("S67890", "CS301", "A-")
    university.assign_grade("S11223", "CS301", "A-")
    university.assign_grade("S11223", "CS202", "B")
    university.assign_grade("S44556", "CS203", "B+")
    university.assign_grade("S44556", "CS204", "A")
    university.assign_grade("S77889", "CS205", "A-")
    university.assign_grade("S77889", "CS206", "B+")
    university.assign_grade("S33445", "CS102", "A")
    university.assign_grade("S33445", "CS207", "A-")
    university.assign_grade("S55667", "CS201", "B")
    university.assign_grade("S55667", "CS202", "B+")
    university.assign_grade("S88990", "CS203", "A")
    university.assign_grade("S88990", "CS204", "A-")
    university.assign_grade("S99001", "CS205", "B+")
    university.assign_grade("S99001", "CS206", "A")
    university.assign_grade("S10203", "CS102", "A-")
    university.assign_grade("S10203", "CS207", "B")
    university.close()
    print("Database initialized with sample data.")

def inspect_database():
    """Initializes the DB, lists all tables, and prints their contents."""
    print("--- Initializing Database for Inspection ---")
    initialize_database()
    print("\n--- Starting Database Inspection ---")
    
    university = University(DB_FILE)
    
    # Get and print all table names
    table_names = university.get_all_table_names()
    print(f"\nTables found in '{DB_FILE}': {table_names}\n")
    
    # Print the contents of each table
    for table in table_names:
        if table == 'sqlite_sequence': # Skip internal sqlite table
            continue
        print(f"--- Contents of table: {table} ---")
        headers, contents = university.get_table_contents(table)
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers)) + 2))
        if not contents:
            print("(No data in this table)")
        else:
            for row in contents:
                print(" | ".join(map(str, row)))
        print("\n" + "="*40 + "\n")
        
    university.close()
    print("--- Database Inspection Complete ---")

if __name__ == "__main__":
    inspect_database()

