import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_projects_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title, ))
    row = DB.fetchone()
    print """
    Project: %s
    Description: %s
    """ % (row[0], row[1])

def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_project_grade(github, title):
    query = """SELECT S.first_name, S.last_name, G.project_title, G.grade
    FROM Grades AS G
        INNER JOIN Students AS S ON (S.github=G.student_github)
    WHERE github = ? AND G.project_title = ?"""
    DB.execute(query, (github,title))
    row = DB.fetchone()
    
    print """
    First name: %s
    Last name: %s
    Project: %s
    Grade: %d""" % (row[0], row[1], row[2], row[3])

def new_project_grade(github, title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?)"""
    DB.execute(query, (github, title, grade))
    CONN.commit()
    print "Successfully added grade of %d to Project %s for %s" % (int(grade), title, github)

def get_grades(github):
    query = """SELECT * FROM Grades WHERE student_github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    for row in rows:
        print """Student: %s, Project: %s, Grade: %d""" % (row[0], row[1], row[2])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_projects_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "project_grade":
            get_project_grade(*args)
        elif command == "new_project_grade":
            new_project_grade(*args)
        elif command == "get_grades":
            get_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
