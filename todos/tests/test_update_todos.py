from todos.serializers import TodoCreateSerializer
from todos.db.services import TodosDBService
import pytest
from fastapi.testclient import TestClient


class TestUpdateTodos:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.url = '/todos'
        self.db_service = TodosDBService()
        self.todo = self.db_service.create_todo(TodoCreateSerializer(
            title='Todo1',
            description='Descrição',
            status='DOING',
            due_date='2021-07-15 00:00',
            responsible='João'
        ))

    def test_update_todos(self, client: TestClient):
        payload = dict(
            title='Todo2',
            description='Descrição2',
            status='DONE',
            due_date='2022-07-15 00:00',
            responsible='João2'
        )
        response = client.put(f'{self.url}/{self.todo.id}/', json=payload,
                              allow_redirects=True)
        print(response.__dict__)
        response_json = response.json()
        print('response_json: ', response_json)
        assert response_json['id'] == self.todo.id
        assert response_json['title'] == 'Todo2'
        assert response_json['description'] == 'Descrição2'
        assert response_json['status'] == 'DONE'
        assert response_json['due_date'] == '2022-07-15T00:00:00+00:00'
        assert response_json['responsible'] == 'João2'
        assert response.status_code == 200

        todos = self.db_service.get_todos()
        assert len(todos) == 1

        todo = todos[0]
        assert todo.id == self.todo.id
        assert todo.title == 'Todo2'
        assert todo.description == 'Descrição2'
        assert todo.status == 'DONE'
        assert todo.due_date.isoformat() == '2022-07-15T00:00:00+00:00'
        assert todo.responsible == 'João2'

    def test_update_todos_invalid_id(self, client: TestClient):
        payload = dict(
            title='Todo2',
            description='Descrição2',
            status='DONE',
            due_date='2022-07-15 00:00',
            responsible='João2'
        )
        response = client.put(f'{self.url}/{self.todo.id}1/', json=payload,
                              allow_redirects=True)
        print(response.__dict__)
        response_json = response.json()
        print('response_json: ', response_json)
        assert response_json['error'] == 'Todo not found.'
        assert response.status_code == 404

        todos = self.db_service.get_todos()
        assert len(todos) == 1

        todo = todos[0]
        assert todo.id == self.todo.id
        assert todo.title == 'Todo1'
        assert todo.description == 'Descrição'
        assert todo.status == 'DOING'
        assert todo.due_date.isoformat() == '2021-07-15T00:00:00+00:00'
        assert todo.responsible == 'João'
