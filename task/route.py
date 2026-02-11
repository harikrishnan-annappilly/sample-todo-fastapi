from fastapi import APIRouter, HTTPException
from task.schema import TaskInput, TaskModel, TaskEditInput

task_router = APIRouter()


@task_router.get("/all")
def show_all_tasks():
    return TaskModel.find_all()


@task_router.post("/all", status_code=201)
def create_task(payload: TaskInput):
    task = TaskModel.model_validate(payload.model_dump())
    task.save()
    return {"msg": "task created", "data": task}


@task_router.get("/one/{task_id}")
def show_one_task(task_id: int):
    return TaskModel.find_one(id=task_id)


@task_router.put("/one/{task_id}")
def edit_one_task(task_id: int, payload: TaskEditInput):
    task = TaskModel.find_one(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="No task found with given id")
    task.title = payload.title if payload.title is not None else task.title
    task.status = payload.status if payload.status is not None else task.status
    task.save()
    return {"msg": f"edited task with {task_id}", "data": task}


@task_router.delete("/one/{task_id}")
def delete_one_task(task_id: int):
    task = TaskModel.find_one(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="No task found with given id")
    task.delete()
    return {"msg": f"deleted task with id {task_id}"}
