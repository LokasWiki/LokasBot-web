from markupsafe import escape

from flask import (
    Blueprint, render_template, url_for, abort
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

    total_count = db_session.query(Page).count()
    status_0_count = db_session.query(Page).filter_by(status=Status.PENDING, task_name=taskname).count()
    status_1_count = db_session.query(Page).filter_by(status=Status.RECEIVED, task_name=taskname).count()
    pages_list = db_session.query(Page).filter_by(status=Status.RECEIVED, task_name=taskname).order_by(
        Page.update_date.asc()).all()

    return render_template("tasks/show.html", total_count=total_count, status_0_count=status_0_count,
                           status_1_count=status_1_count, pages_list=pages_list,
                           all_url=url_for('tasks.task_index', name=name))
