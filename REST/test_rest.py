import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# GET: List all items
def get_items():
    response = requests.get(f"{BASE_URL}/items")
    print("GET /items:", response.status_code, response.json())

# GET: Retrieve a specific item
def get_item(item_id):
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    print(f"GET /items/{item_id}:", response.status_code, response.json())

# POST: Create a new item
def create_item():
    new_item = {
        "name": "New Item", 
        "description": "Description of the new item"
    }
    response = requests.post(f"{BASE_URL}/items", json=new_item)
    print("POST /items:", response.status_code, response.json())

# PUT: Update an existing item
def update_item(item_id):
    updated_item = {"name": "Updated Item", "description": "Updated description"}
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item)
    print(f"PUT /items/{item_id}:", response.status_code, response.json())

# DELETE: Delete an item
def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print(f"DELETE /items/{item_id}:", response.status_code)

# Mini demo
if __name__ == "__main__":
    print("Starting API test...\n")

    # 1. List all items
    get_items()

    # 2. Create a new item
    create_item()

    # 3. List all items again to verify creation
    get_items()

    # 4. Retrieve the first item
    get_item(1)

    # 5. Update the first item
    update_item(1)

    # 6. Retrieve the updated item
    get_item(1)

    # 7. Delete the first item
    delete_item(1)

    # 8. List all items to confirm deletion
    get_items()

    print("\nAPI test completed.")
