from todos.serializers import TodoCreateSerializer
import pytest
from fastapi.testclient import TestClient
from todos.db.services import TodosDBService


class TestGetTodo:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.url = '/todos'
        self.todo = TodosDBService().create_todo(TodoCreateSerializer(
            title='Todo1',
            description='Descrição',
            status='DOING',
            due_date='2021-07-15 00:00',
            responsible='João'
        ))

    def test_get_todo(self, client: TestClient):
        response = client.get(f'{self.url}/{self.todo.id}/',
                              allow_redirects=True)
        response_json = response.json()
        print('response_json: ', response_json)
        assert response_json['id'] == self.todo.id
        assert response_json['title'] == 'Todo1'
        assert response_json['description'] == 'Descrição'
        assert response_json['status'] == 'DOING'
        assert response_json['due_date'] == '2021-07-15T00:00:00+00:00'
        assert response_json['responsible'] == 'João'
        assert response.status_code == 200

    def test_get_todo_not_found(self, client: TestClient):
        response = client.get(f'{self.url}/{self.todo.id}1/',
                              allow_redirects=True)
        response_json = response.json()
        print('response_json: ', response_json)
        assert response_json['error'] == 'Todo not found.'
        assert response.status_code == 404
