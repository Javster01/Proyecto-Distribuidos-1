from flask import Blueprint, request, jsonify, current_app

# Define el Blueprint
bp = Blueprint('main', __name__)

@bp.route('/items', methods=['GET'])
def get_items():
    # Usa current_app para acceder a la conexión MySQL
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return jsonify(items), 200

@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if item:
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        'name': data['name'],
        'quantity': data['quantity'],
        'price': data['price']
    }
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)",
                   (new_item['name'], new_item['quantity'], new_item['price']))
    current_app.mysql.connection.commit()
    new_item['id'] = cursor.lastrowid
    return jsonify(new_item), 201

@bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    updated_item = {
        'name': data['name'],
        'quantity': data['quantity'],
        'price': data['price']
    }
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("UPDATE items SET name = %s, quantity = %s, price = %s WHERE id = %s",
                   (updated_item['name'], updated_item['quantity'], updated_item['price'], item_id))
    current_app.mysql.connection.commit()
    if cursor.rowcount:
        return jsonify(updated_item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    current_app.mysql.connection.commit()
    if cursor.rowcount:
        return '', 204
    else:
        return jsonify({'error': 'Item not found'}), 404
