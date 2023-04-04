import enum
from datetime import datetime

from sqlalchemy import String, func, INTEGER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.databases.database import Base


class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"


class TaskName(enum.Enum):
    MAINTENANCE = "maintenance"
    WEBCITE = "webcite"


class Page(Base):
    __tablename__ = "pages"
    # todo: comment columns will add in next version
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    thread_number: Mapped[int] = mapped_column(INTEGER)
    status: Mapped[Status] = mapped_column(insert_default=Status.PENDING)

    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
    task_name: Mapped[TaskName] = mapped_column(insert_default=TaskName.MAINTENANCE)

    def __repr__(self) -> str:
        return f"pages(id={self.id!r}, title={self.title!r})"
