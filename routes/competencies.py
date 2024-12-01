from flask import Blueprint, request, jsonify
from database import db
from models import Competency, EmployeeCompetency, RoleCompetency, Course

competencies_blueprint = Blueprint('competencies', __name__)

# 1. Fetch Competencies for an Employee
@competencies_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_competencies(employee_id):
    employee_competencies = EmployeeCompetency.query.filter_by(employee_id=employee_id).all()
    result = [
        {
            "competency_id": ec.competency_id,
            "name": ec.competency.name,
            "description": ec.competency.description,
            "type": ec.competency.type,
            "status": ec.status,
            "expiry_date": ec.competency.expiry_date
        } for ec in employee_competencies
    ]
    return jsonify(result), 200

# 2. Update Competency Status for an Employee
@competencies_blueprint.route('/employee/<int:employee_id>', methods=['PUT'])
def update_employee_competency_status(employee_id):
    data = request.get_json()
    competency_id = data['competency_id']
    status = data['status']

    employee_competency = EmployeeCompetency.query.filter_by(
        employee_id=employee_id, competency_id=competency_id
    ).first()

    if employee_competency:
        employee_competency.status = status
        db.session.commit()
        return jsonify({"message": "Competency status updated successfully"}), 200
    else:
        return jsonify({"error": "Competency not found for employee"}), 404

# 3. Add Competency for a Role
@competencies_blueprint.route('/role', methods=['POST'])
def add_role_competency():
    data = request.get_json()
    role_name = data['role_name']
    competency_id = data['competency_id']

    role_competency = RoleCompetency(role_name=role_name, competency_id=competency_id)
    db.session.add(role_competency)
    db.session.commit()

    return jsonify({"message": "Competency added to role"}), 201

# 4. Fetch Suggested Courses for a Competency
@competencies_blueprint.route('/courses/<int:competency_id>', methods=['GET'])
def get_courses_for_competency(competency_id):
    courses = Course.query.filter_by(competency_id=competency_id).all()
    result = [
        {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "platform": course.platform,
            "url": course.url
        } for course in courses
    ]
    return jsonify(result), 200
