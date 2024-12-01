from flask import Blueprint, request, jsonify
from database import db
from models import Employee, User

employee_blueprint = Blueprint('employees', __name__)

@employee_blueprint.route('/', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'GET':
        employees = Employee.query.all()
        result = [
            {
                "id": emp.id,
                "name": emp.name,
                "skills": emp.skills,
                "certifications": emp.certifications,
                "manager_id": emp.manager_id
            } for emp in employees
        ]
        return jsonify(result), 200

    if request.method == 'POST':
        data = request.get_json()
        new_employee = Employee(
            name=data['name'],
            skills=data.get('skills'),
            certifications=data.get('certifications'),
            manager_id=data.get('manager_id')
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee created successfully"}), 201

@employee_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee_operations(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            "id": employee.id,
            "name": employee.name,
            "skills": employee.skills,
            "certifications": employee.certifications,
            "manager_id": employee.manager_id
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        employee.name = data.get('name', employee.name)
        employee.skills = data.get('skills', employee.skills)
        employee.certifications = data.get('certifications', employee.certifications)
        employee.manager_id = data.get('manager_id', employee.manager_id)
        db.session.commit()
        return jsonify({"message": "Employee updated successfully"}), 200

    if request.method == 'DELETE':
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully"}), 200
