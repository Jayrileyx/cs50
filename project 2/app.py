from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, g
from flask_cors import CORS
import sqlite3
from datetime import datetime
from db import (
    init_db,
    get_groomers_by_city,
    get_groomer_by_id,
    save_appointment,
    generate_time_slots,
    get_available_slots_by_groomer
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_PATH = "dog_groomers.db"
CORS(app)

# ---------- Database connection helpers ----------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# ---------- User Registration ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            return "All fields are required.", 400

        password_hash = generate_password_hash(password)
        db = get_db()
        try:
            db.execute(
                "INSERT INTO clients (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return "Username or email already registered.", 400

        return redirect(url_for('login'))

    return render_template('register.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        client = db.execute("SELECT * FROM clients WHERE username = ?", (username,)).fetchone()

        if client and check_password_hash(client['password_hash'], password):
            session['client_id'] = client['id']
            flash("Login successful!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('my_appointments'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- Search Groomers ----------
@app.route('/search', methods=['GET'])
def search():
    city = request.args.get('city', '').strip().lower()
    results = get_groomers_by_city(DB_PATH, city)
    return render_template("search_results.html", city=city, groomers=results)

# ---------- Schedule View ----------
@app.route('/schedule/<int:groomer_id>')
def schedule(groomer_id):
    groomer = get_groomer_by_id(DB_PATH, groomer_id)
    slots = get_available_slots_by_groomer(DB_PATH, groomer_id)

    formatted_slots = []
    for slot in slots:
        slot_id, groomer_id, date, time, is_booked, available = slot
        try:
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
        except ValueError:
            formatted_time = time
        formatted_slots.append({
            'id': slot_id,
            'date': date,
            'time': formatted_time
        })

    return render_template('schedule.html', groomer=groomer, available_slots=formatted_slots)

@app.route('/book/<int:groomer_id>', methods=['GET'])
def book(groomer_id):
    # Get groomer info
    db = get_db()
    groomer = db.execute("SELECT * FROM groomers WHERE id = ?", (groomer_id,)).fetchone()

    if groomer is None:
        return "Groomer not found.", 404

    # Get available slots for that groomer
    slots = db.execute("""
        SELECT * FROM slots
        WHERE groomer_id = ? AND available = 1
        ORDER BY start_time
    """, (groomer_id,)).fetchall()

    return render_template("book.html", groomer=groomer, slots=slots)


@app.route('/book', methods=['POST'])
def book_appointment():
    if 'client_id' not in session:
        return redirect(url_for('login', next=url_for('book_appointment')))

    groomer_id = request.form.get('groomer_id')
    slot_id = request.form.get('slot_id')

    db = get_db()
    slot = db.execute("SELECT * FROM slots WHERE id = ? AND available = 1", (slot_id,)).fetchone()

    if slot is None:
        return "Invalid or unavailable slot."

    client_id = session['client_id']
    date = slot['date']
    time = slot['time']

    db.execute("""
        INSERT INTO appointments (groomer_id, slot_id, client_id, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (groomer_id, slot_id, client_id, date, time))

    db.execute("UPDATE slots SET is_booked = 1, available = 0 WHERE id = ?", (slot_id,))
    db.commit()

    return redirect(url_for('my_appointments'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# ---------- My Appointments ----------
@app.route('/my_appointments')
def my_appointments():
    if 'client_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    appointments = db.execute("""
        SELECT a.date, a.time, g.name AS groomer_name
        FROM appointments a
        JOIN groomers g ON a.groomer_id = g.id
        WHERE a.client_id = ?
        ORDER BY a.date, a.time
    """, (session['client_id'],)).fetchall()

    return render_template('my_appointments.html', appointments=appointments)

# ---------- Main ----------
if __name__ == '__main__':
    init_db(DB_PATH)
    generate_time_slots(DB_PATH)
    app.run(debug=True)

