from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='jon'
    )

@app.route('/alumnos', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM alumnos')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

@app.route('/alumnos', methods=['POST'])
def create_item():
    new_item = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO alumnos (nombre, apellido, curso) VALUES (%s, %s, %s)',
        (new_item['nombre'], new_item['apellido'], new_item['curso'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_item), 201

@app.route('/alumnos/<int:alumno_id>', methods=['PUT'])
def update_item(alumno_id):
    updated_item = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE alumnos SET nombre = %s, apellido = %s, curso = %s WHERE id = %s',
        (updated_item['nombre'], updated_item['apellido'], updated_item['curso'], alumno_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(updated_item)

@app.route('/alumnos/<int:alumno_id>', methods=['DELETE'])
def delete_item(alumno_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM alumnos WHERE id = %s', (alumno_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
