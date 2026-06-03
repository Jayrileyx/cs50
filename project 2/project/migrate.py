import sqlite3

DB_PATH = "database.db"  # Change if your DB file is in a different location

def add_available_column():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("ALTER TABLE slots ADD COLUMN available INTEGER DEFAULT 1")
        print("✅ Column 'available' added to 'slots' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("ℹ️ Column 'available' already exists.")
        else:
            raise
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    add_available_column()
