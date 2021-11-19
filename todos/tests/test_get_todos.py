from todos.serializers import TodoCreateSerializer
import pytest
from fastapi.testclient import TestClient
from todos.db.services import TodosDBService


class TestGetTodos:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.url = '/todos/'
        self.todo1 = TodosDBService().create_todo(TodoCreateSerializer(
            title='Todo1',
            description='Descrição',
            status='DOING',
            due_date='2021-07-15 00:00',
            responsible='João'
        ))
        self.todo2 = TodosDBService().create_todo(TodoCreateSerializer(
            title='Todo2',
            description='Descrição2',
            status='DONE',
            due_date='2022-07-15 00:00',
            responsible='João2'
        ))

    def test_get_todos(self, client: TestClient):
        response = client.get(self.url, allow_redirects=True)
        response_json = response.json()
        print('response_json: ', response_json)
        assert len(response_json) == 2
        for todo in response_json:
            assert todo.get('id') in [self.todo1.id, self.todo2.id]
            assert todo.get('title') in ['Todo1', 'Todo2']
            assert todo.get('description') in ['Descrição', 'Descrição2']
            assert todo.get('status') in ['DOING', 'DONE']
            assert todo.get('due_date') in ['2021-07-15T00:00:00+00:00', '2022-07-15T00:00:00+00:00']
            assert todo.get('responsible') in ['João', 'João2']
        assert response.status_code == 200
