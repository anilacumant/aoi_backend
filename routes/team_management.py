from flask import Blueprint, jsonify
from models import Employee

team_management_blueprint = Blueprint('team_management', __name__)

@team_management_blueprint.route('/employees/<int:manager_id>', methods=['GET'])
def get_team_employees(manager_id):
    """
    Fetch employees reporting to the given manager.
    """
    try:
        employees = Employee.query.filter_by(manager_id=manager_id).all()
        if not employees:
            return jsonify({"message": "No employees found for the manager"}), 404
        
        result = [
            {
                "id": emp.id,
                "name": emp.name,
                "skills": emp.skills,
                "certifications": emp.certifications
            }
            for emp in employees
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
