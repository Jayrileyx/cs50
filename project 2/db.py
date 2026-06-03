import sqlite3
from datetime import datetime, timedelta

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Clients table (with password_hash for security)
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Groomers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS groomers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            rating REAL
        )
    ''')

    # Slots table (separate date/time, and available flag)
    c.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            groomer_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0,
            available INTEGER DEFAULT 1,
            FOREIGN KEY (groomer_id) REFERENCES groomers(id)
        )
    ''')

    # Appointments table (also storing date/time for history)
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            groomer_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (groomer_id) REFERENCES groomers(id),
            FOREIGN KEY (slot_id) REFERENCES slots(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    conn.commit()
    conn.close()


def generate_time_slots(db_path, days_ahead=7):
    """Generate 30-minute slots for each groomer if not already present."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id FROM groomers")
    groomer_ids = [row[0] for row in c.fetchall()]

    for groomer_id in groomer_ids:
        for day_offset in range(days_ahead):
            date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            for hour in range(8, 17):  # 8:00 AM - 4:30 PM
                for minute in (0, 30):
                    time_str = f"{hour:02d}:{minute:02d}"

                    # Check if already exists
                    c.execute("""
                        SELECT 1 FROM slots
                        WHERE groomer_id = ? AND date = ? AND time = ?
                    """, (groomer_id, date, time_str))

                    if not c.fetchone():
                        c.execute("""
                            INSERT INTO slots (groomer_id, date, time, is_booked, available)
                            VALUES (?, ?, ?, 0, 1)
                        """, (groomer_id, date, time_str))

    conn.commit()
    conn.close()


def get_groomers_by_city(db_path, city):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, address, phone, rating FROM groomers WHERE LOWER(city) = ?", (city.lower(),))
    rows = c.fetchall()
    conn.close()
    return [
        {"id": row[0], "name": row[1], "address": row[2], "phone": row[3], "rating": row[4]}
        for row in rows
    ]


def get_groomer_by_id(db_path, groomer_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, address, phone, rating FROM groomers WHERE id = ?", (groomer_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "address": row[2], "phone": row[3], "rating": row[4]}
    return None


def get_available_slots_by_groomer(db_path, groomer_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT id, groomer_id, date, time, is_booked, available
        FROM slots
        WHERE groomer_id = ? AND available = 1
        ORDER BY date, time
    """, (groomer_id,))
    slots = c.fetchall()
    conn.close()
    return slots


def save_appointment(db_path, groomer_id, slot_id, client_id, date, time):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        INSERT INTO appointments (groomer_id, slot_id, client_id, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (groomer_id, slot_id, client_id, date, time))

    c.execute("""
        UPDATE slots
        SET is_booked = 1, available = 0
        WHERE id = ?
    """, (slot_id,))

    conn.commit()
    conn.close()

