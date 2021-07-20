from mangum import Mangum
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db.services import DBService
from todos.views import todo_router
from pynamodb.exceptions import TableError
from time import sleep


app = FastAPI(
    title='Todo Aplication',
)


@app.get('/')
def status():
    return dict(status='OK')


app.include_router(
    todo_router,
    prefix='/todos',
    tags=['todos']
)


@app.on_event("startup")
async def startup_event():
    while(True):
        try:
            DBService.create_tables()
        except TableError:
            print('DynamoDB não está disponível ainda - Espere...')
            sleep(1)
        else:
            break


@app.exception_handler(Exception)
async def handle_all_exceptions(request: Request, error: Exception):
    return JSONResponse(
        status_code=500,
        content=str(error),
    )

handler = Mangum(app)
