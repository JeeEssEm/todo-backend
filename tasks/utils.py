from .schemes import TaskScheme


async def task_scheme_converter(task_obj):
    desc = None
    if task_obj.description is not None:
        desc = task_obj.description[:50] + '...'

    return TaskScheme(
        title=task_obj.title,
        description=desc,
        task_status=task_obj.status,
        task_importance=task_obj.importance,
        reminder=task_obj.reminder
    )
