from src.application.dto import TaskShortInfo, TastStatus
from src.application.interfaces import TasksRepository


class PostgresTasksRepository(TasksRepository):
    def __init__(self, connection):
        self._connection = connection
        self._connection.autocommit = True

    def create(self, text_link: str) -> int:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tasks (link, status) VALUES (%s, %s) RETURNING id;",
                    (text_link, TastStatus.PROCESSING.value),
                )

                return cursor.fetchone()[0]

    def get_all(self) -> list[TaskShortInfo]:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT id, link, status FROM tasks;")
                rows = cursor.fetchall()

                return [
                    TaskShortInfo(id=row[0], link=row[1], status=TastStatus[row[2]])
                    for row in rows
                ]
