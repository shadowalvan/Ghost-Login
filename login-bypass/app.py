from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("INSERT OR IGNORE INTO users VALUES(1,'admin','admin123')")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        # Vulnerable query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = c.execute(query).fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    flag = "FTA{sql_login_bypass_success}"
    return render_template("dashboard.html", flag=flag)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)