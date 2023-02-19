import os
from markupsafe import escape

from flask import Flask, render_template, request, url_for, abort
import sqlite3

app = Flask(__name__)

__dir__ = os.path.dirname(__file__)


def get_db(name):
    # This will create a pages.db file in the home directory of the user running the script.
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, name)
    conn = sqlite3.connect(database_path)
    return conn.cursor()


def to_dict(row):
    status = "في الانتظار"
    if row[2] == 1:
        status = "جاري العمل"

    return {
        'id': row[0],
        'link': '<a  target="_blank"  href="https://ar.wikipedia.org/wiki/' + row[1] + '">' + row[1] + '</a>',
        'status': status,
        'data': row[3]
    }


@app.route('/')
def index():
    return render_template("home.html")


@app.route("/tasks/<name>")
def task_index(name):
    if escape(name) not in ["maintenance", "webcite"]:
        abort(404)

    cursor = get_db(escape(name) + ".db")

    cursor.execute("SELECT COUNT(*) FROM pages")
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 0")
    status_0_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages WHERE status = 1")
    status_1_count = cursor.fetchone()[0]
    cursor.execute("SELECT title,date FROM pages WHERE status = 1 ORDER BY date ASC")
    pages_list = cursor.fetchall()
    return render_template("index.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list, all_url=url_for('list_of_pages_in_tasks',name=name))


@app.route("/tasks/<name>/pages")
def list_of_pages_in_tasks(name):
    if escape(name) not in ["maintenance", "webcite"]:
        abort(404)

    return render_template("pages.html", name=name)


@app.route('/api/tasks/<name>/pages/data')
def pages_list_api(name):
    if escape(name) not in ["maintenance", "webcite"]:
        abort(404)

    cursor = get_db(escape(name) + ".db")

    pages = cursor.execute("SELECT id,title, status, date FROM pages LIMIT 100").fetchall()

    return {'data': [to_dict(page) for page in pages]}


if __name__ == "main":
    app.run()
