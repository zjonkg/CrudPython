from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='jon'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(alumnos)


@app.route('/alumnos', methods=['POST'])
def create_alumno():
    new_alumno = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO alumnos (nombre, apellido, curso) VALUES (%s, %s, %s)',
        (new_alumno['nombre'], new_alumno['apellido'], new_alumno['curso'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_alumno), 201


@app.route('/alumnos/<int:alumno_id>', methods=['PUT'])
def update_alumno(alumno_id):
    updated_alumno = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE alumnos SET nombre = %s, apellido = %s, curso = %s WHERE id = %s',
        (updated_alumno['nombre'], updated_alumno['apellido'], updated_alumno['curso'], alumno_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(updated_alumno)


@app.route('/alumnos/<int:alumno_id>', methods=['DELETE'])
def delete_alumno(alumno_id):
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
