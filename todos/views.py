# from common.serializers import ErrorSerializer
from todos.db.services import TodosDBService
from todos.db.models import TodoModel
from fastapi import APIRouter
from .serializers import TodoCreateSerializer, TodoUpdateSerializer
from fastapi.responses import JSONResponse

todo_router = APIRouter()
database = TodosDBService()

'''
GET todos/
'''


@todo_router.get('/')
def get_todos():
    todos = database.get_todos()
    return todos


''''
GET todos/{id}/
'''


@todo_router.get('/{id}/')
def get_todo(id: str):
    try:
        todo = database.get_todo(id)
        return todo
    except TodoModel.DoesNotExist:
        return JSONResponse(status_code=404, content=dict(
                                error='Todo not found.'))


'''
POST todos
'''


@todo_router.post('/', status_code=201)
def create_todo(todo: TodoCreateSerializer):
    return database.create_todo(todo)


'''
PUT todos
'''


@todo_router.put('/{id}/')
def update_todo(id: str, todo: TodoUpdateSerializer):
    try:
        update = database.update_todo(id, todo)
        return update
    except TodoModel.DoesNotExist:
        return JSONResponse(status_code=404, content=dict(
                                error='Todo not found.')
                            )


''''
DELETE todos/{id}/
'''


@todo_router.delete('/{id}/', status_code=204)
def delete_todo(id: str):
    try:
        delete = database.delete_todo(id)
        return delete
    except TodoModel.DoesNotExist:
        return JSONResponse(status_code=404, content=dict(
                                error='Todo not found.')
                            )
