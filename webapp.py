from flask import Flask, render_template, request, redirect, url_for
import hackbright_app

app = Flask(__name__)

@app.route("/")
def index():
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
    project_description = hackbright_app.get_projects_by_title(project_title)
    student_grade_rows = hackbright_app.get_project_grade_all_students(project_title)

    html = render_template("project_grades.html", project_title=project_title,
                                                  description=project_description[1],
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
        html = render_template("index.html")
        return html

@app.route("/createNewProject")
def create_new_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("title")
    project_description = request.args.get("description")
    max_grade = request.args.get("max_grade")

    result = hackbright_app.make_new_project(project_title,project_description,max_grade)
    
    if result == True and project_title != None:
        return redirect(url_for('get_project_grades_all_students', project=project_title))  
    else:
        html = render_template("index.html")
        return html

@app.route("/createNewGrade")
def create_new_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    project_title= request.args.get("project_title")
    grade = request.args.get("grade")

    result = hackbright_app.new_project_grade(student_github,project_title,grade)
    
    if result == True and project_title != None:
        return redirect(url_for('get_student', github=student_github))  
    else:
        html = render_template("index.html")
        return html

if __name__ == "__main__":
    app.run(debug=True)