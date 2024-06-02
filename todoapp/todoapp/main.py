from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Annotated
from todoapp import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string, connect_args={}, pool_recycle=300)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Hello World API with DB", version="0.0.1", servers=[
    {
        "url": "http://127.0.0.1:8000",
        "description": "Development Server"
    }
])

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo: Todo, session: Annotated[Session, Depends(get_session)], todo_id: int):
    todo_db = session.get(Todo, todo_id)
    if todo_db is None:
        return {"error": "Todo not found"}
    todo_db.content = todo.content
    session.add(todo_db)
    session.commit()
    return todo_db

@app.delete("/todos/{todo_id}", response_model=dict[str, str])
async def delete_todo(session: Annotated[Session, Depends(get_session)], todo_id: int):
    todo_db = session.get(Todo, todo_id)
    if todo_db is None:
        return {"error": "Todo not found"}
    session.delete(todo_db)
    session.commit()
    return {"message": f"Todo with id {todo_id} deleted successfully"}