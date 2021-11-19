from db.services import DBService
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from todos.serializers import TodoSerializer
from db.models import BaseModel


class TodoModel(BaseModel):
    title: str = UnicodeAttribute()
    description: str = UnicodeAttribute()
    status: str = UnicodeAttribute()
    responsible: str = UnicodeAttribute()
    due_date: str = UTCDateTimeAttribute()

    class Meta:
        table_name = DBService.table_name('todo')
        host = DBService.host()

    @property
    def serialized(self):
        return TodoSerializer.from_orm(self)
