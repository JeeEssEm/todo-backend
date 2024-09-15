from .schemes import TaskScheme


async def task_scheme_converter(task_obj):
    desc = None
    date = None
    if task_obj.description is not None:
        desc = task_obj.description[:50] + '...'
    if task_obj.reminder is not None:
        date = task_obj.reminder.timestamp()

    return TaskScheme(
        id=task_obj.id,
        title=task_obj.title,
        description=desc,
        task_status=task_obj.status,
        task_importance=task_obj.importance,
        reminder=date
    )


async def task_json_converter(task_obj):
    date = None
    if task_obj.reminder is not None:
        date = task_obj.reminder.timestamp()
    return {
        'id': task_obj.id,
        'title': task_obj.title,
        'description': task_obj.description,
        'status': task_obj.status.value,
        'importance': task_obj.importance.value,
        'reminder': date,
        'xp': task_obj.xp
    }
