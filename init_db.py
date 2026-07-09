
import sqlite3

conn = sqlite3.connect("booking.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Movies Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    show_time TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT
)
""")

# Seats Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS seats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    seat_number TEXT,
    status TEXT DEFAULT 'available',
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
""")

# Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    seat_number TEXT,
    amount REAL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Admin Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Default Admin
cursor.execute("""
INSERT OR IGNORE INTO admins(username,password)
VALUES('admin','admin123')
""")

# Sample Movies
cursor.execute("SELECT COUNT(*) FROM movies")
count = cursor.fetchone()[0]

if count == 0:
    movies = [
        ("Interstellar","03:30 PM",250,
        "https://picsum.photos/400/250?1"),

        ("Inception","06:00 PM",300,
        "https://picsum.photos/400/250?2"),

        ("Avengers Endgame","09:00 PM",350,
        "https://picsum.photos/400/250?3")
    ]

    cursor.executemany("""
    INSERT INTO movies(title,show_time,price,image)
    VALUES(?,?,?,?)
    """,movies)

    # Create Seats
    cursor.execute("SELECT id FROM movies")
    movie_ids = cursor.fetchall()

    for movie in movie_ids:

        movie_id = movie[0]

        rows = ['A','B','C','D','E']

        for row in rows:
            for num in range(1,11):

                seat = f"{row}{num}"

                cursor.execute("""
                INSERT INTO seats(movie_id,seat_number,status)
                VALUES(?,?,?)
                """,(movie_id,seat,'available'))

conn.commit()
conn.close()

print("Database Created Successfully")

