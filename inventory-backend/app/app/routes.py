from flask import Blueprint, request, jsonify, current_app

# Define el Blueprint
bp = Blueprint('main', __name__)

@bp.route('/items', methods=['GET'])
def get_items():
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    print("Fetched items:", items)  # Log de los items obtenidos
    return jsonify(items), 200

@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    if item:
        print("Fetched item:", item)  # Log del item obtenido
        return jsonify(item), 200
    else:
        print("Item not found:", item_id)  # Log de item no encontrado
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
    print("Created item:", new_item)  # Log del item creado
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
        print("Updated item:", updated_item)  # Log del item actualizado
        return jsonify(updated_item), 200
    else:
        print("Item not found for update:", item_id)  # Log de item no encontrado para actualización
        return jsonify({'error': 'Item not found'}), 404

@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    current_app.mysql.connection.commit()
    if cursor.rowcount:
        print("Deleted item:", item_id)  # Log del item eliminado
        return '', 204
    else:
        print("Item not found for deletion:", item_id)  # Log de item no encontrado para eliminación
        return jsonify({'error': 'Item not found'}), 404