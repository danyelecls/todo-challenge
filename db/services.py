import os
import logging
from pynamodb.constants import HOST
from common.enums import EnvironmentSet
from pynamodb.settings import get_settings_value

ENVIRONMENT: EnvironmentSet = os.environ.get('ENVIRONMENT')


class DBService:
    @staticmethod
    def create_tables():
        if ENVIRONMENT != EnvironmentSet.PRODUCTION:
            from todos.db.models import TodoModel
            tables = [
                TodoModel
            ]
            for table in tables:
                if not table.exists():
                    logging.info(f'CREATING TABLE ==> {table.Meta.__dict__}')
                    table.create_table(
                        wait=True,
                        read_capacity_units=1,
                        write_capacity_units=1
                    )

    @staticmethod
    def destroy_tables():
        if ENVIRONMENT != EnvironmentSet.PRODUCTION:
            from todos.db.models import TodoModel
            tables = [
                TodoModel
            ]
            for table in tables:
                if table.exists():
                    logging.info(f'DESTROYING TABLE ==> {table.Meta.__dict__}')
                    table.delete_table()

    @staticmethod
    def table_name(table_name: str):
        return f'{ENVIRONMENT}_{table_name}'

    @staticmethod
    def host():
        return 'http://pubnic-todo-dynamodb:8000' if (
            ENVIRONMENT != EnvironmentSet.PRODUCTION
        ) else get_settings_value(HOST)
