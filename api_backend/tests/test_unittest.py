from fastapi.testclient import TestClient
from main import app  # Adjust the import according to your project structure

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of items

def test_add_item():
    item = {"name": "Test Item", "quantity": 10, "price": 5.99}
    response = client.post("/items/", json=item)
    assert response.status_code == 200
    assert response.json() == item

def test_read_item():
    # This test assumes that an item has been added first
    response = client.get("/items/0")
    assert response.status_code == 200
    # Make sure to adjust the assertion based on the actual structure of your data
    assert "name" in response.json()

def test_update_item():
    item = {"name": "Updated Test Item", "quantity": 20, "price": 10.99}
    # Assuming an item exists at index 0
    response = client.put("/items/0", json=item)
    assert response.status_code == 200
    assert response.json() == item

def test_delete_item():
    # This test assumes that an item exists at index 0
    response = client.delete("/items/0")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

def test_upload_file():
    files = {'file': ('data.xlsx', open('data.xlsx', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}
