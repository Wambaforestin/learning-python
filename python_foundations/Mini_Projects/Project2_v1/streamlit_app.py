"""
A Streamlit web application for the University Management System.
"""
import streamlit as st
import pandas as pd
from db_logic import University, initialize_database, DB_FILE

# --- Page Configuration ---
st.set_page_config(
    page_title="University Management System",
    page_icon="🎓",
    layout="wide"
)

# --- Database Connection ---
# Use a session state to cache the database connection
if 'db' not in st.session_state:
    st.session_state.db = University(DB_FILE)

db = st.session_state.db

# --- Page Title ---
st.title("University Management System")

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Manage People",
    "Manage Courses",
    "Enrollments & Grades",
    "System"
])
st.sidebar.markdown("---")
st.sidebar.info("This is a demo application showcasing a university management system using Streamlit and SQLite.")


# --- Page: Dashboard ---
if page == "Dashboard":
    st.header("Dashboard")
    st.markdown("Welcome to the University Management System. Here's a quick overview.")

    col1, col2, col3 = st.columns(3)

    students = db.get_people('student')
    professors = db.get_people('professor')
    courses = db.get_courses()

    with col1:
        st.metric("Total Students", len(students))
    with col2:
        st.metric("Total Professors", len(professors))
    with col3:
        st.metric("Total Courses", len(courses))

    st.markdown("---")

    st.subheader("All Courses")
    if courses:
        df_courses = pd.DataFrame(courses, columns=["Course Name", "Course Code", "Professor"])
        st.dataframe(df_courses, use_container_width=True)
    else:
        st.info("No courses found.")

# --- Page: Manage People ---
elif page == "Manage People":
    st.header("Manage People")

    tab1, tab2 = st.tabs(["Students", "Professors"])

    with tab1:
        st.subheader("Add New Student")
        with st.form("add_student_form", clear_on_submit=True):
            s_name = st.text_input("Name")
            s_age = st.number_input("Age", min_value=16, max_value=100)
            s_id = st.text_input("Student ID (e.g., S12345)")
            submitted_s = st.form_submit_button("Add Student")
            if submitted_s and s_name and s_id:
                message = db.add_student(s_name, s_age, s_id)
                st.success(message)
            elif submitted_s:
                st.warning("Please fill in all fields.")

        st.subheader("Existing Students")
        students = db.get_people('student')
        if students:
            df_students = pd.DataFrame(students, columns=["Name", "Age", "Student ID"])
            st.dataframe(df_students, use_container_width=True)
        else:
            st.info("No students found.")

    with tab2:
        st.subheader("Add New Professor")
        with st.form("add_prof_form", clear_on_submit=True):
            p_name = st.text_input("Name")
            p_age = st.number_input("Age", min_value=25, max_value=100)
            p_id = st.text_input("Employee ID (e.g., P54321)")
            submitted_p = st.form_submit_button("Add Professor")
            if submitted_p and p_name and p_id:
                message = db.add_professor(p_name, p_age, p_id)
                st.success(message)
            elif submitted_p:
                st.warning("Please fill in all fields.")

        st.subheader("Existing Professors")
        professors = db.get_people('professor')
        if professors:
            df_profs = pd.DataFrame(professors, columns=["Name", "Age", "Employee ID"])
            st.dataframe(df_profs, use_container_width=True)
        else:
            st.info("No professors found.")

# --- Page: Manage Courses ---
elif page == "Manage Courses":
    st.header("Manage Courses")

    st.subheader("Add New Course")
    with st.form("add_course_form", clear_on_submit=True):
        c_name = st.text_input("Course Name")
        c_code = st.text_input("Course Code (e.g., CS101)")
        submitted_c = st.form_submit_button("Add Course")
        if submitted_c and c_name and c_code:
            message = db.add_course(c_name, c_code)
            st.success(message)
        elif submitted_c:
            st.warning("Please fill in all fields.")

    st.subheader("Assign Professor to Course")
    professors = db.get_people('professor')
    courses = db.get_courses()

    if professors and courses:
        prof_options = {f"{p[0]} ({p[2]})": p[2] for p in professors}
        course_options = {f"{c[0]} ({c[1]})": c[1] for c in courses}

        selected_prof_display = st.selectbox("Select Professor", list(prof_options.keys()))
        selected_course_display = st.selectbox("Select Course", list(course_options.keys()))

        if st.button("Assign Professor"):
            prof_id = prof_options[selected_prof_display]
            course_code = course_options[selected_course_display]
            message = db.assign_professor_to_course(prof_id, course_code)
            st.success(message)
            st.rerun() # Refresh the page to show updated course list
    else:
        st.warning("Please add professors and courses first.")

    st.subheader("All Courses")
    courses_refreshed = db.get_courses() # Re-fetch courses to show updates
    if courses_refreshed:
        df_courses = pd.DataFrame(courses_refreshed, columns=["Course Name", "Course Code", "Professor"])
        st.dataframe(df_courses, use_container_width=True)
    else:
        st.info("No courses found.")


# --- Page: Enrollments & Grades ---
elif page == "Enrollments & Grades":
    st.header("Enrollments & Grades")

    tab1, tab2, tab3 = st.tabs(["Enroll Student", "Assign Grade", "View Records"])

    with tab1:
        st.subheader("Enroll Student in a Course")
        students = db.get_people('student')
        courses = db.get_courses()

        if students and courses:
            student_options = {f"{s[0]} ({s[2]})": s[2] for s in students}
            course_options = {f"{c[0]} ({c[1]})": c[1] for c in courses}

            selected_student_display = st.selectbox("Select Student", list(student_options.keys()), key="enroll_student")
            selected_course_display = st.selectbox("Select Course", list(course_options.keys()), key="enroll_course")

            if st.button("Enroll Student"):
                student_id = student_options[selected_student_display]
                course_code = course_options[selected_course_display]
                message = db.enroll_student_in_course(student_id, course_code)
                st.success(message)
        else:
            st.warning("Please add students and courses first.")

    with tab2:
        st.subheader("Assign a Grade")
        students = db.get_people('student')
        courses = db.get_courses()

        if students and courses:
            student_options = {f"{s[0]} ({s[2]})": s[2] for s in students}
            course_options = {f"{c[0]} ({c[1]})": c[1] for c in courses}

            selected_student_display = st.selectbox("Select Student", list(student_options.keys()), key="grade_student")
            selected_course_display = st.selectbox("Select Course", list(course_options.keys()), key="grade_course")
            grade = st.text_input("Grade (e.g., A, B+, C-)")

            if st.button("Assign Grade"):
                if grade:
                    student_id = student_options[selected_student_display]
                    course_code = course_options[selected_course_display]
                    message = db.assign_grade(student_id, course_code, grade)
                    st.success(message)
                else:
                    st.warning("Please enter a grade.")
        else:
            st.warning("Please add students and courses first.")

    with tab3:
        st.subheader("View Course Summary")
        courses = db.get_courses()
        if courses:
            course_options = {f"{c[0]} ({c[1]})": c[1] for c in courses}
            selected_course_display = st.selectbox("Select a course to view its summary", list(course_options.keys()))
            if selected_course_display:
                course_code = course_options[selected_course_display]
                enrolled_students = db.get_course_summary(course_code)
                if enrolled_students:
                    df_enrolled = pd.DataFrame(enrolled_students, columns=["Student Name", "Student ID"])
                    st.dataframe(df_enrolled, use_container_width=True)
                else:
                    st.info("No students are enrolled in this course.")

        st.markdown("---")

        st.subheader("View Student Grades")
        students = db.get_people('student')
        if students:
            student_options = {f"{s[0]} ({s[2]})": s[2] for s in students}
            selected_student_display = st.selectbox("Select a student to view their grades", list(student_options.keys()))
            if selected_student_display:
                student_id = student_options[selected_student_display]
                grades = db.get_student_grades(student_id)
                if grades:
                    df_grades = pd.DataFrame(grades, columns=["Course Name", "Course Code", "Grade"])
                    st.dataframe(df_grades, use_container_width=True)
                else:
                    st.info("This student has no grades recorded.")

# --- Page: System ---
elif page == "System":
    st.header("System Management")
    st.warning("Warning: This will delete all existing data and create a new database with sample entries.")
    if st.button("Initialize/Reset Database with Sample Data"):
        # Close the existing connection before deleting the file
        st.session_state.db.close()
        
        # Now, initialize the database (which includes deleting the old file)
        initialize_database()
        
        # Re-establish the connection and store the new object in the session state
        st.session_state.db = University(DB_FILE)
        st.success("Database has been reset and initialized with sample data!")
        st.info("Application reconnected to the new database. Refreshing...")
        st.rerun()

