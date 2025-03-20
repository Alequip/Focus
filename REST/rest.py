from flask import Flask, jsonify, request

app = Flask(__name__)
    
data = [
    {"id": 1, "name": "Item 1", "description": "Description of item 1"},
    {"id": 2, "name": "Item 2", "description": "Description of item 2"}
]

# GET (http://127.0.0.1:5000/items)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data), 200

# FETCH 1 elemento (http://127.0.0.1:5000/items/2)
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    if not new_item or 'name' not in new_item or 'description' not in new_item:
        return jsonify({"error": "Invalid data"}), 400

    new_id = max(item['id'] for item in data) + 1 if data else 1
    new_item['id'] = new_id
    data.append(new_item)
    return jsonify(new_item), 201

# UPDATE
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    update_data = request.get_json()
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    if not update_data or 'name' not in update_data or 'description' not in update_data:
        return jsonify({"error": "Invalid data"}), 400

    item.update(update_data)
    return jsonify(item), 200

# DELETE
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
