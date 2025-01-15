import typing

from src.application import dto


class TasksRepository(typing.Protocol):
    def create(self, text_link: str) -> int: ...

    def get_all(self) -> list[dto.TaskShortInfo]: ...


class TasksTextRepository(typing.Protocol):
    def load(self, text: str) -> str: ...

    def get(self, link: str) -> str: ...


class TasksWorker(typing.Protocol):
    def add(self, task_id: int): ...
