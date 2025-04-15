from fastapi.testclient import TestClient

def test_find_all(use_fixture: TestClient):
    """
    Test the find_all function.
    """
    response = use_fixture.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Assuming there are 2 items in the fixture

def test_find_by_id_202(use_fixture: TestClient):
    """
    Test the find_by_id function.
    """
    response = use_fixture.get("/items/select/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_find_by_id_404(use_fixture: TestClient):
    # Non-existing item
    response = use_fixture.get("/items/select/999")
    assert response.status_code == 404

    #user_id false
    response = use_fixture.get("/items/select/2")
    assert response.status_code == 404

def test_find_by_name_200(use_fixture: TestClient):
    """
    Test the find_by_name function.
    """
    response = use_fixture.get("/items/search?name=testitem2")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Assuming there is 1 item with the name "testitem2"
    assert response.json()[0]["name"] == "testitem2"

def test_find_by_name_404(use_fixture: TestClient):
    """
    Test the find_by_name function.
    """
    response = use_fixture.get("/items/search?name=nonexistent")
    assert response.status_code == 404

def test_create_item_201(use_fixture: TestClient):
    """
    Test the create_item function.
    """
    new_item = {
        "name": "newitem",
        "price": 150,
        "description": "newdescription",
        "status": "ON_SALE"
    }
    response = use_fixture.post("/items/create", json=new_item)
    assert response.status_code == 201
    assert response.json()["name"] == "newitem"
    assert response.json()["id"] == 3  # Assuming the new item gets ID 3

    response = use_fixture.get("/items")
    assert len(response.json()) == 3

def test_create_item_400(use_fixture: TestClient):
    """
    Test the create_item function.
    """
    new_item = {
        "name": "newitem",
        "price": -150,  # Invalid price
        "description": "newdescription",
        "status": "ON_SALE"
    }
    response = use_fixture.post("/items/create", json=new_item)
    assert response.status_code == 400  # Unprocessable Entity for invalid data

def test_update_item_200(use_fixture: TestClient):
    """
    Test the update_item function.
    """
    updated_item = {
        "name": "updateditem",
        "price": 250,
        "description": "updateddescription",
        "status": "OUT_OF_STOCK"
    }
    response = use_fixture.put("/items/update/1", json=updated_item)
    assert response.status_code == 200
    assert response.json()["name"] == "updateditem"
    assert response.json()["price"] == 250

def test_update_item_404(use_fixture: TestClient):
    """
    Test the update_item function.
    """
    updated_item = {
        "name": "updateditem",
        "price": 250,
        "description": "updateddescription",
        "status": "OUT_OF_STOCK"
    }
    response = use_fixture.put("/items/update/999", json=updated_item)  # Non-existing item
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item_200(use_fixture: TestClient):
    """
    Test the delete_item function.
    """
    response = use_fixture.delete("/items/delete/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = use_fixture.get("/items")
    assert len(response.json()) == 1  # Assuming one item was deleted

def test_delete_item_404(use_fixture: TestClient):
    """
    Test the delete_item function.
    """
    response = use_fixture.delete("/items/delete/999")  # Non-existing item
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
