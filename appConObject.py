from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/jon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model definition with class name capitalized
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    curso = db.Column(db.String(5), nullable=False)

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    alumnos_list = [{'id': alumno.id, 'nombre': alumno.nombre, 'apellido': alumno.apellido, 'curso': alumno.curso} for alumno in alumnos]
    return jsonify(alumnos_list)

@app.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.json
    new_alumno = Alumno(nombre=data['nombre'], apellido=data.get('apellido'), curso=data.get('curso'))
    db.session.add(new_alumno)
    db.session.commit()
    return jsonify({'id': new_alumno.id, 'nombre': new_alumno.nombre, 'apellido': new_alumno.apellido, 'curso': new_alumno.curso}), 201

@app.route('/alumnos/<int:alumno_id>', methods=['PUT'])
def update_alumno(alumno_id):
    data = request.json
    alumno = Alumno.query.get_or_404(alumno_id)
    alumno.nombre = data['nombre']
    alumno.apellido = data.get('apellido')
    alumno.curso = data.get('curso')
    db.session.commit()
    return jsonify({'id': alumno.id, 'nombre': alumno.nombre, 'apellido': alumno.apellido, 'curso': alumno.curso})

@app.route('/alumnos/<int:alumno_id>', methods=['DELETE'])
def delete_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    db.session.delete(alumno)
    db.session.commit()
    return '', 204  

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
