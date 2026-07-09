from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import qrcode
import os

os.makedirs("static/qr", exist_ok=True)
import uuid

ticket_id = str(uuid.uuid4())[:8]

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("booking.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return render_template("home.html", movies=movies)

@app.route("/test")
def test():
    return "TEST WORKING"

@app.route("/movie/<int:id>")
def movie_details(id):
    conn = get_db()
    movie = conn.execute(
        "SELECT * FROM movies WHERE id=?",
        (id,)
    ).fetchone()
    conn.close()

    return render_template(
        "movie_details.html",
        movie=movie
    )

@app.route("/select-seat/<int:movie_id>")
def select_seat(movie_id):
    conn = get_db()

    movie = conn.execute(
        "SELECT * FROM movies WHERE id=?",
        (movie_id,)
    ).fetchone()

    seats = conn.execute(
        "SELECT * FROM seats WHERE movie_id=?",
        (movie_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "seat_selection.html",
        movie=movie,
        seats=seats
    )

@app.route("/payment/<int:movie_id>", methods=["POST"])
def payment(movie_id):

    seats = request.form.get("selected_seats")

    conn = get_db()

    movie = conn.execute(
        "SELECT * FROM movies WHERE id=?",
        (movie_id,)
    ).fetchone()

    qr_data = f"""
Movie : {movie['title']}
Seats : {seats}
Price : ₹{movie['price']}
"""

    qr = qrcode.make(qr_data)

    qr_path = f"static/qr/movie_{movie_id}.png"

    qr.save(qr_path)

    conn.close()

    return render_template(
        "payment.html",
        seats=seats,
        movie=movie,
        qr_image=qr_path
    )
if __name__ == "__main__":
    app.run(debug=True)
