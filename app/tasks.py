from flask import (
    Blueprint, render_template, url_for, abort, request, jsonify
)
from markupsafe import escape

from app.databases.database import db_session
from app.databases.models import Page, Status, TaskName

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/show/<name>')
def task_index(name):
    if escape(name).strip().lower() not in ["maintenance", "webcite"]:
        abort(404)
    taskname = TaskName.MAINTENANCE
    if name == "webcite":
        taskname = TaskName.WEBCITE

    total_count = db_session.query(Page).filter_by(task_name=taskname).count()
    status_0_count = db_session.query(Page).filter_by(status=Status.PENDING, task_name=taskname).count()
    status_1_count = db_session.query(Page).filter_by(status=Status.RECEIVED, task_name=taskname).count()
    pages_list = db_session.query(Page).filter_by(status=Status.RECEIVED, task_name=taskname).order_by(
        Page.update_date.asc()).all()

    return render_template("tasks/show.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list,
                           all_url=url_for('tasks.list_of_pages_in_tasks', name=name))


@bp.route("/show/<name>/pages")
def list_of_pages_in_tasks(name):
    if escape(name) not in ["maintenance", "webcite"]:
        abort(404)
    return render_template("tasks/pages.html", name=name)


@bp.route('/api/tasks/<name>/pages/data')
def pages_list_api(name):
    if name not in [TaskName.MAINTENANCE.value, TaskName.WEBCITE.value]:
        abort(404)

    query = Page.query.filter(Page.task_name == TaskName[escape(name).upper()])

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter((Page.title.like(f"%{search}%")) | (Page.thread_number == int(search)))

    total_filtered = query.count()

    # ordering
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ["id", "title", "status", "create_date", "update_date", "thread_number"]:
            col_name = 'id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        order.append(getattr(getattr(Page, col_name), "desc" if descending else "asc")())
        i += 1

    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    pages = query.limit(length).offset(start).all()

    return jsonify({
        'data': [page.to_dict() for page in pages],
        'recordsFiltered': total_filtered,
        'recordsTotal': query.count(),
        'draw': request.args.get('draw', type=int),
    })
