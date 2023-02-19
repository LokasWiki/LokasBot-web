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
        'page_id': row[0],
        'link': row[1],
        'status': status,
        'data': row[3],
        "thread": row[4]
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
    cursor.execute("SELECT title,date,thread FROM pages WHERE status = 1 ORDER BY date ASC")
    pages_list = cursor.fetchall()
    return render_template("index.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list,
                           all_url=url_for('list_of_pages_in_tasks', name=name))


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

    query = ""
    # search filter
    search = request.args.get('search[value]')
    if search:
        query += f" where title like '%{search}%' "
        query += f" or title thread ={search} "

    cursor.execute(f"SELECT COUNT(*) FROM pages {query}")
    total_filtered = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pages")
    recordsTotal = cursor.fetchone()[0]

    order_str = ""
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ["id","title", "status", "date","thread"]:
            col_name = 'id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        order_str += f"{col_name} {('desc' if descending else 'asc')},"
        i += 1

    if order_str:
        order_str = " ORDER BY " + order_str[:-1]  # remove the trailing comma and add ORDER BY

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query_res = f"SELECT id,title, status, date,thread FROM pages {query} {order_str} LIMIT {length} OFFSET {start}"
    pages = cursor.execute(query_res).fetchall()

    return {
        'data': [to_dict(page) for page in pages],
        'recordsFiltered': total_filtered,
        'recordsTotal': recordsTotal,
        'draw': request.args.get('draw', type=int),
    }


if __name__ == "main":
    app.run()
