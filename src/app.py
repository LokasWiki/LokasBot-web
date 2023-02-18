import os

from flask import Flask, render_template, request, url_for
import sqlite3

app = Flask(__name__)


def get_db(name):
    # This will create a pages.db file in the home directory of the user running the script.
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, name)
    conn = sqlite3.connect(database_path)
    return conn.cursor()


@app.route('/')
def index():
    return render_template("home.html")


@app.route("/maintenance")
def maintenance_index():
    cursor = get_db("maintenance.db")

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute("SELECT COUNT(*) FROM pages")
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 0")
    status_0_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 1")
    status_1_count = cursor.fetchone()[0]
    cursor.execute("SELECT title FROM pages WHERE status = 0 ORDER BY date ASC LIMIT 50")
    pages_list = cursor.fetchall()
    return render_template("pages.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list,all_url=url_for('maintenance_pages'))


@app.route("/maintenance/pages")
def maintenance_pages():
    cursor = get_db("maintenance.db")

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    page = request.args.get("page", 1, type=int)
    per_page = 100
    cursor.execute("SELECT COUNT(*) FROM pages")
    total_count = cursor.fetchone()[0]
    pages = cursor.execute("SELECT title, status, date FROM pages LIMIT ? OFFSET ?",
                           (per_page, (page - 1) * per_page)).fetchall()
    return render_template("index.html", pages=pages, total_count=total_count, page=page, per_page=per_page)


@app.route("/webcite")
def webcite_index():
    cursor = get_db("webcite.db")

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute("SELECT COUNT(*) FROM pages")
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 0")
    status_0_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 1")
    status_1_count = cursor.fetchone()[0]
    cursor.execute("SELECT title FROM pages WHERE status = 0 ORDER BY date ASC LIMIT 50")
    pages_list = cursor.fetchall()
    return render_template("pages.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list,all_url=url_for('webcite_pages'))


@app.route("/webcite/pages")
def webcite_pages():
    cursor = get_db("webcite.db")

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    page = request.args.get("page", 1, type=int)
    per_page = 100
    cursor.execute("SELECT COUNT(*) FROM pages")
    total_count = cursor.fetchone()[0]
    pages = cursor.execute("SELECT title, status, date FROM pages LIMIT ? OFFSET ?",
                           (per_page, (page - 1) * per_page)).fetchall()
    return render_template("index.html", pages=pages, total_count=total_count, page=page, per_page=per_page)


if __name__ == "main":
    app.run()
