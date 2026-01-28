from flask import Flask, request, session, redirect
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "weak_secret_key"  # ضعيف عمداً

LOG_FILE = "logs.txt"

def log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {event}\n")

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin','admin123')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = u
            log(f"LOGIN SUCCESS | user={u} | session={request.cookies.get('session')}")
            return redirect("/dashboard")
        else:
            log(f"LOGIN FAILED | user={u}")
            return "Login Failed"

    return '''
    <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit">
    </form>
    '''

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        log(f"DASHBOARD ACCESS | user={session['user']} | session={request.cookies.get('session')}")
        return f"Welcome {session['user']} (Authenticated)"
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
