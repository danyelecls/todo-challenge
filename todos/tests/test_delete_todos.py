from todos.serializers import TodoCreateSerializer
from todos.db.services import TodosDBService
import pytest
from fastapi.testclient import TestClient


class TestDeleteTodos:
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

    def test_delete_todos(self, client: TestClient):
        assert len(self.db_service.get_todos()) == 1
        response = client.delete(f'{self.url}/{self.todo.id}/',
                                 allow_redirects=True)
        assert len(self.db_service.get_todos()) == 0
        assert response.status_code == 204

    def test_delete_not_exist(self, client: TestClient):
        response = client.delete(f'{self.url}/{self.todo.id}1/',
                                 allow_redirects=True)
        response_json = response.json()
        print('response_json: ', response_json)
        assert response_json['error'] == 'Todo not found.'
        assert response.status_code == 404

        todos = self.db_service.get_todos()
        assert len(todos) == 1
