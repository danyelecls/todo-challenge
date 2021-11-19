from uuid import uuid4
from pynamodb.exceptions import DoesNotExist
from todos.serializers import TodoCreateSerializer, TodoUpdateSerializer
from todos.db.models import TodoModel


class TodosDBService:
    def get_todos(self):
        todos = TodoModel.scan()
        return [todo.serialized for todo in todos]

    def get_todo(self, id: str):
        todo = TodoModel.get(id)
        return todo.serialized

    def create_todo(self, todo_serializer: TodoCreateSerializer):
        todo = TodoModel(
            str(uuid4()),
            **todo_serializer.dict()
        )
        todo.save()
        return todo.serialized

    def update_todo(self, id: str, todo_serializer: TodoUpdateSerializer):
        todo_model = TodoModel.get(id)
        todo_model.update(actions=[
            TodoModel.title.set(todo_serializer.title),
            TodoModel.responsible.set(todo_serializer.responsible),
            TodoModel.description.set(todo_serializer.description),
            TodoModel.due_date.set(todo_serializer.due_date),
            TodoModel.status.set(todo_serializer.status)
        ])
        return todo_model.serialized

    def delete_todo(self, id: str):
        todo = TodoModel.get(id)
        todo.delete()
        return True
