from flask import Blueprint, request, jsonify
from database import db
from models import LearningResource, EmployeeLearning

learning_blueprint = Blueprint('learning', __name__)

@learning_blueprint.route('/resources', methods=['GET'])
def get_learning_resources():
    resources = LearningResource.query.all()
    result = [
        {
            "id": res.id,
            "name": res.name,
            "type": res.type,
            "description": res.description,
            "url": res.url,
            "competency_id": res.competency_id
        } for res in resources
    ]
    return jsonify(result), 200

@learning_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_learning(employee_id):
    learning_records = EmployeeLearning.query.filter_by(employee_id=employee_id).all()
    result = [
        {
            "id": rec.id,
            "resource_name": rec.resource.name,
            "progress": rec.progress
        } for rec in learning_records
    ]
    return jsonify(result), 200
