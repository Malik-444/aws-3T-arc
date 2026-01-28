#This work without RDS and uses memomry to store 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple ToDo API")

# In-memory database for demo purposes
todos = []

# Pydantic model for validation
class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI 3-tier app!"}

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todos

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    # Check for duplicate ID
    if any(t.id == todo.id for t in todos):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists.")
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated: TodoItem):
    for idx, t in enumerate(todos):
        if t.id == todo_id:
            todos[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for idx, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(idx)
            return {"message": f"Todo {todo_id} deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
