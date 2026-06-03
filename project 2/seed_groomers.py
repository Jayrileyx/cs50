import sqlite3
from db import init_db, generate_time_slots

DB_PATH = "dog_groomers.db"

# Step 1: Make sure the database and tables exist
init_db(DB_PATH)

# Step 2: Add groomers
groomers = [
    ("Paws & Relax", "Houston", "123 Main St", "555-1234", 4.7),
    ("Furry Friends Grooming", "Houston", "456 Oak St", "555-5678", 4.5),
    ("Luxe Pups", "Austin", "789 Maple Ave", "555-8765", 4.8),
    ("Bark Avenue", "Austin", "321 Pine Rd", "555-4321", 4.6),
    ("The Dog Spa", "Dallas", "654 Elm St", "555-2468", 4.9),
    ("Happy Tails", "Dallas", "987 Birch Blvd", "555-1357", 4.4),
    ("Groom & Zoom", "San Antonio", "159 Cedar Dr", "555-9753", 4.3),
    ("Pampered Pooch", "San Antonio", "753 Spruce Ln", "555-8642", 4.6),
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executemany("""
    INSERT INTO groomers (name, city, address, phone, rating)
    VALUES (?, ?, ?, ?, ?)
""", groomers)

conn.commit()
conn.close()

# Step 3: Generate slots for these groomers
generate_time_slots(DB_PATH, days_ahead=7)

print("✅ Groomers and slots added successfully!")
