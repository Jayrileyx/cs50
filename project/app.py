from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database setup

def init_db():
    conn = sqlite3.connect("groomie.db")
    c = conn.cursor()

    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )""")

    # Bookings table
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    city TEXT NOT NULL,
                    groomer_name TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    UNIQUE(city, groomer_name, time_slot),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )""")
    conn.commit()
    conn.close()


# Preloaded groomers
groomers = {
    "Houston": [
        {
            "name": "Pawfect Style Grooming",
            "address": "1234 Westheimer Rd, Houston, TX 77006",
            "phone": "(713) 555-1234",
            "rating": 4.7,
            "description": "Full-service grooming with organic shampoos, styling, and nail trimming.",
            "image": "/static/images/pawfect-style.jpg"
        },
        {
            "name": "Furry Friends Spa",
            "address": "5678 Kirby Dr, Houston, TX 77005",
            "phone": "(713) 555-5678",
            "rating": 4.9,
            "description": "Luxury grooming with aromatherapy, coat conditioning, and spa treatments.",
            "image": "/static/images/furry-friends.jpg"
        },
        {
            "name": "The Groom Room",
            "address": "910 Shepherd Dr, Houston, TX 77007",
            "phone": "(713) 555-9101",
            "rating": 4.6,
            "description": "Affordable and friendly grooming with fast turnaround times.",
            "image": "/static/images/groom-room.jpg"
        }
    ],
    "Dallas": [
        {
            "name": "Paws & Relax",
            "address": "321 Main St, Dallas, TX 75201",
            "phone": "(214) 555-3210",
            "rating": 4.8,
            "description": "Relaxing grooming with calming music and all-natural products.",
            "image": "/static/images/paws-relax.jpg"
        },
        {
            "name": "Tail Waggers Grooming",
            "address": "654 Elm St, Dallas, TX 75202",
            "phone": "(214) 555-6543",
            "rating": 4.5,
            "description": "Expert grooming for all breeds with a focus on style and comfort.",
            "image": "/static/images/tail-waggers.jpg"
        }
    ],
    "Austin": [
        {
            "name": "Bark Avenue",
            "address": "1111 Congress Ave, Austin, TX 78701",
            "phone": "(512) 555-1111",
            "rating": 4.9,
            "description": "Upscale grooming with spa treatments and breed-specific styling.",
            "image": "/static/images/bark-avenue.jpg"
        },
        {
            "name": "Happy Tails Grooming",
            "address": "2222 Barton Springs Rd, Austin, TX 78704",
            "phone": "(512) 555-2222",
            "rating": 4.6,
            "description": "Fun and friendly grooming experience with plenty of treats.",
            "image": "/static/images/happy-tails.jpg"
        }
    ],
    "San Antonio": [
        {
            "name": "The Doggy Spa",
            "address": "777 Market St, San Antonio, TX 78205",
            "phone": "(210) 555-7777",
            "rating": 4.8,
            "description": "Luxury dog spa offering massages, grooming, and pawdicures.",
            "image": "/static/images/doggy-spa.jpg"
        },
        {
            "name": "Shaggy Chic Groomers",
            "address": "888 Riverwalk St, San Antonio, TX 78205",
            "phone": "(210) 555-8888",
            "rating": 4.5,
            "description": "Trendy grooming salon with stylish cuts and coat coloring.",
            "image": "/static/images/shaggy-chic.jpg"
        }
    ]
}

def get_time_slots():
    """Generate times from 8:00 AM to 5:00 PM every 30 minutes."""
    slots = []
    start = datetime.strptime("08:00", "%H:%M")
    end = datetime.strptime("17:00", "%H:%M")
    while start <= end:
        slots.append(start.strftime("%I:%M %p"))
        start += timedelta(minutes=30)
    return slots


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect("groomie.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, hashed_pw))
            conn.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = sqlite3.connect("groomie.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect(url_for("choose_city"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/choose_city", methods=["GET", "POST"])
def choose_city():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        city = request.form["city"]
        return redirect(url_for("list_groomers", city=city))
    return render_template("choose_city.html", cities=list(groomers.keys()))


@app.route("/groomers/<city>")
def list_groomers(city):
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("groomers.html", city=city, groomers=groomers[city])


@app.route("/book/<city>/<groomer>", methods=["GET", "POST"])
def book(city, groomer):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]

        # Check if slot already taken
        exists = conn.execute(
            "SELECT * FROM appointments WHERE city = ? AND groomer = ? AND date = ? AND time = ?",
            (city, groomer, date, time)
        ).fetchone()

        if exists:
            flash("Sorry, that time slot is already booked.", "danger")
            conn.close()
            return redirect(url_for("book", city=city, groomer=groomer))

        # Save booking
        conn.execute(
            "INSERT INTO appointments (user_id, city, groomer, date, time) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], city, groomer, date, time)
        )
        conn.commit()
        conn.close()

        flash("Appointment booked successfully!", "success")
        return redirect(url_for("appointments"))

    # GET request → show booking form
    return render_template("book.html", city=city, groomer=groomer)


@app.route("/confirmation")
def confirmation():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("groomie.db")
    c = conn.cursor()
    c.execute("""SELECT city, groomer_name, time_slot
                 FROM bookings WHERE user_id = ?""",
              (session["user_id"],))
    my_bookings = c.fetchall()
    conn.close()

    return render_template("confirmation.html", bookings=my_bookings)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/appointments")
def appointments():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    appts = conn.execute(
        "SELECT * FROM appointments WHERE user_id = ? ORDER BY date, time",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("appointments.html", appointments=appts)


@app.route("/cancel/<int:appointment_id>", methods=["POST"])
def cancel(appointment_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute(
        "DELETE FROM appointments WHERE id = ? AND user_id = ?",
        (appointment_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    flash("Appointment cancelled successfully.", "success")
    return redirect(url_for("appointments"))


@app.route("/reschedule/<int:appointment_id>", methods=["POST", "GET"])
def reschedule(appointment_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        new_time = request.form.get("time")
        date = request.form.get("date")

        # Check if slot is free
        exists = conn.execute(
            "SELECT * FROM appointments WHERE date = ? AND time = ?",
            (date, new_time)
        ).fetchone()

        if exists:
            flash("That time slot is already booked. Choose another.", "danger")
            conn.close()
            return redirect(url_for("reschedule", appointment_id=appointment_id))

        conn.execute(
            "UPDATE appointments SET date = ?, time = ? WHERE id = ? AND user_id = ?",
            (date, new_time, appointment_id, session["user_id"])
        )
        conn.commit()
        conn.close()

        flash("Appointment rescheduled successfully.", "success")
        return redirect(url_for("appointments"))

    # GET request → show reschedule form
    appt = conn.execute(
        "SELECT * FROM appointments WHERE id = ? AND user_id = ?",
        (appointment_id, session["user_id"])
    ).fetchone()
    conn.close()

    if not appt:
        flash("Appointment not found.", "danger")
        return redirect(url_for("appointments"))

    return render_template("reschedule.html", appointment=appt)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
