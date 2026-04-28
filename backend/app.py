from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/data', methods=['GET'])
def get_data():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title}), 201

@app.route('/api/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return '', 204

@app.route('/')
def info():
    return "Backend by Salima Abdyrasakova (COMCEH-23)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
