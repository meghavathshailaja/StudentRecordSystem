
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create the database
def init_db():
    conn = sqlite3.connect("students.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add student page
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        year = request.form["year"]

        conn = sqlite3.connect("students.db")
        conn.execute(
            "INSERT INTO students (name, department, year) VALUES (?, ?, ?)",
            (name, department, year)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("view_students"))

    return render_template("add_student.html")


# View students page
@app.route("/students")
def view_students():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template(
        "view_students.html",
        students=students
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
