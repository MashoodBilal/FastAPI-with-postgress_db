

from fastapi.testclient import TestClient
import json
from ..todoapp.main import app, Todo  # Import the FastAPI app and Todo model

# Test the root route (/)
def test_read_root():
    client = TestClient(app)  # Create a TestClient instance for the app
    response = client.get("/")  # Send a GET request to the root route
    assert response.status_code == 200  # Check if the response status code is 200
    assert response.json() == {"Hello": "World"}  # Check if the response JSON matches the expected output

# Test creating a new Todo item (/todos/)
def test_create_todo():
    client = TestClient(app)  # Create a TestClient instance for the app
    todo = {"content": "Test Todo"}  # Define a sample Todo item
    response = client.post("/todos/", json/todo)  # Send a POST request to create a new Todo item
    assert response.status_code == 201  # Check if the response status code is 201 (Created)
    todo_db = response.json()  # Get the created Todo item from the response JSON
    assert todo_db["id"] is not None  # Check if the Todo item ID is not None

# Test reading a single Todo item (/todos/{todo_id})
def test_read_todo():
    client = TestClient(app)  # Create a TestClient instance for the app
    todo_id = 1  # Define a sample Todo item ID
    response = client.get(f"/todos/{todo_id}")  # Send a GET request to read a single Todo item
    assert response.status_code == 200  # Check if the...


# Test updating a Todo item (/todos/{todo_id})
def test_update_todo():
    client = TestClient(app)
    todo_id = 1
    todo = {"content": "Updated Todo"}
    response = client.put(f"/todos/{todo_id}", json=todo)  # Send a PUT request to update a Todo item
    assert response.status_code == 200  # Check if the response status code is 200 (OK)
    updated_todo = response.json()
    assert updated_todo["content"] == "Updated Todo"  # Check if the updated Todo item content matches

# Test deleting a Todo item (/todos/{todo_id})
def test_delete_todo():
    client = TestClient(app)
    todo_id = 1
    response = client.delete(f"/todos/{todo_id}")  # Send a DELETE request to delete a Todo item
    assert response.status_code == 200  # Check if the response status code is 200 (OK)

# Run all tests
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_read_root())
    loop.run_until_complete(test_create_todo())
    loop.run_until_complete(test_read_todo())
    loop.run_until_complete(test_update_todo())
    loop.run_until_complete(test_delete_todo())
    loop.close()