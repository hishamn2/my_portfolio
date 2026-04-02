import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    # FIXED: Corrected path and indentation
    db_path = '/home/Hichamn2/my_portfolio/project.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template("index.html", projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        content = request.form.get("message")

        db = get_db_connection()
        db.execute("INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
                   (name, email, content))
        db.commit()
        db.close()
        return redirect(url_for('index'))

    return render_template("contact.html")

# ALWAYS AT THE BOTTOM
if __name__ == "__main__":
    app.run(debug=True)
