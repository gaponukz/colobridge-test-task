import dataclasses
import enum


class TastStatus(enum.StrEnum):
    PROCESSING = "PROCESSING"
    DONE = "DONE"


@dataclasses.dataclass
class CreateTaskInputDTO:
    text: str


@dataclasses.dataclass
class CreateTaskOutputDTO:
    task_id: int
    status: TastStatus


@dataclasses.dataclass
class TaskShortInfo:
    id: int
    link: str
    status: TastStatus


@dataclasses.dataclass
class TaskFullInfo(TaskShortInfo):
    text: str


@dataclasses.dataclass
class GetTasksOutputDTO:
    tasks: list[TaskFullInfo]
