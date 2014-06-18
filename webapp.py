from flask import Flask, render_template, request, redirect, url_for
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("index.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student_info_row = hackbright_app.get_student_by_github(student_github)
    project_grades_rows = hackbright_app.get_grades(student_github)

    html = render_template("student_info.html", first_name=student_info_row[0],
                                                last_name=student_info_row[1],
                                                github=student_info_row[2],
                                                projects=project_grades_rows)

    return html

@app.route("/project")
def get_project_grades_all_students():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    student_grade_rows = hackbright_app.get_project_grade_all_students(project_title)

    html = render_template("project_grades.html", project_title=project_title,
                                                  students=student_grade_rows)

    return html

@app.route("/createNewStudent")
def create_new_student():
    hackbright_app.connect_to_db()
    student_first_name = request.args.get("first_name")
    student_last_name = request.args.get("last_name")
    student_github = request.args.get("github")
    result = hackbright_app.make_new_student(student_first_name, student_last_name, student_github)
    if result == True and student_first_name != None:
        return redirect(url_for('get_student', github=student_github))  
    else:
        html = render_template("new_student.html")
        return html

@app.route("/createNewProject")
def create_new_project():
    hackbright_app.connect_to_db()
    
    result = hackbright_app.make_new_student(student_first_name, student_last_name, student_github)
    
    html = render_template("success.html")

    return html

if __name__ == "__main__":
    app.run(debug=True)