from src.application import dto
from src.application.interfaces import TasksRepository, TasksTextRepository, TasksWorker


def create_task(
    task: dto.CreateTaskInputDTO,
    repo: TasksRepository,
    text_repo: TasksTextRepository,
    worker: TasksWorker,
) -> dto.CreateTaskOutputDTO:

    link = text_repo.load(task.text)
    task_id = repo.create(link)
    worker.add(task_id)

    return dto.CreateTaskOutputDTO(
        task_id=task_id,
        status=dto.TastStatus.PROCESSING,
    )


def get_tasks(
    repo: TasksRepository, text_repo: TasksTextRepository
) -> dto.GetTasksOutputDTO:
    tasks = []

    for task in repo.get_all():
        tasks.append(
            dto.TaskFullInfo(
                id=task.id,
                link=task.link,
                status=task.status,
                text=text_repo.get(task.link),
            )
        )

    return dto.GetTasksOutputDTO(tasks)
