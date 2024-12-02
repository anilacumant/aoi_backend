from flask import Blueprint, request, jsonify
from database import db
from models import Employee, CertificationRequest, User

employee_blueprint = Blueprint('employees', __name__)
users_blueprint = Blueprint('users', __name__)

# Fetch all employees with associated manager names
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
                "manager_id": emp.manager_id,
                "manager_name": User.query.get(emp.manager_id).username if emp.manager_id else "Unassigned"
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

# Employee CRUD operations
@employee_blueprint.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee_operations(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            "id": employee.id,
            "name": employee.name,
            "skills": employee.skills,
            "certifications": employee.certifications,
            "manager_id": employee.manager_id,
            "manager_name": User.query.get(employee.manager_id).username if employee.manager_id else "Unassigned"
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
        try:
            db.session.delete(employee)
            db.session.commit()
            return jsonify({"message": "Employee deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

# Fetch all managers
@users_blueprint.route('/managers/', methods=['GET'])
def get_managers():
    try:
        managers = User.query.filter_by(role='Manager').all()
        result = [
            {
                "id": manager.id,
                "username": manager.username
            } for manager in managers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
