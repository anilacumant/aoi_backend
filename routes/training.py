from flask import Blueprint, request, jsonify
from database import db
from models import Training

training_blueprint = Blueprint('training', __name__)

@training_blueprint.route('/<int:employee_id>', methods=['GET'])
def get_training(employee_id):
    trainings = Training.query.filter_by(employee_id=employee_id).all()
    result = [
        {
            "id": train.id,
            "program_name": train.program_name,
            "status": train.status
        } for train in trainings
    ]
    return jsonify(result), 200

@training_blueprint.route('/', methods=['POST'])
def add_training():
    data = request.get_json()
    new_training = Training(
        employee_id=data['employee_id'],
        program_name=data['program_name'],
        status=data.get('status', 'In-progress')
    )
    db.session.add(new_training)
    db.session.commit()
    return jsonify({"message": "Training added successfully"}), 201

@training_blueprint.route('/status', methods=['PUT'])
def update_training_status():
    data = request.get_json()
    training = Training.query.get_or_404(data['id'])
    training.status = data['status']
    db.session.commit()
    return jsonify({"message": "Training status updated successfully"}), 200
