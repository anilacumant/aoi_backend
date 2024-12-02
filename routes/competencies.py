from flask import Blueprint, request, jsonify
from database import db
from models import Competency, EmployeeCompetency, RoleCompetency, Course

competencies_blueprint = Blueprint('competencies', __name__)

# 1. Fetch All Competencies
@competencies_blueprint.route('/', methods=['GET'])
def get_all_competencies():
    try:
        competencies = Competency.query.all()
        result = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "type": c.type,
                "expiry_date": c.expiry_date,
                "notification_sent": c.notification_sent,
            }
            for c in competencies
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Fetch Competencies for an Employee
@competencies_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_competencies(employee_id):
    try:
        employee_competencies = EmployeeCompetency.query.filter_by(employee_id=employee_id).all()
        result = [
            {
                "competency_id": ec.competency_id,
                "name": ec.competency.name,
                "description": ec.competency.description,
                "type": ec.competency.type,
                "status": ec.status,
                "expiry_date": ec.competency.expiry_date,
            }
            for ec in employee_competencies
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Add a New Competency
@competencies_blueprint.route('/', methods=['POST'])
def add_competency():
    try:
        data = request.get_json()
        new_competency = Competency(
            name=data['name'],
            description=data['description'],
            type=data['type'],
            expiry_date=data.get('expiry_date'),
        )
        db.session.add(new_competency)
        db.session.commit()
        return jsonify({"message": "Competency added successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Update Competency Details
@competencies_blueprint.route('/<int:competency_id>', methods=['PUT'])
def update_competency(competency_id):
    try:
        data = request.get_json()
        competency = Competency.query.get_or_404(competency_id)
        competency.name = data['name']
        competency.description = data['description']
        competency.type = data['type']
        competency.expiry_date = data.get('expiry_date')
        db.session.commit()
        return jsonify({"message": "Competency updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. Assign Competency to a Role
@competencies_blueprint.route('/role', methods=['POST'])
def add_role_competency():
    try:
        data = request.get_json()
        role_name = data['role_name']
        competency_id = data['competency_id']

        role_competency = RoleCompetency(role_name=role_name, competency_id=competency_id)
        db.session.add(role_competency)
        db.session.commit()

        return jsonify({"message": "Competency added to role"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6. Fetch Suggested Courses for a Competency
@competencies_blueprint.route('/courses/<int:competency_id>', methods=['GET'])
def get_courses_for_competency(competency_id):
    try:
        courses = Course.query.filter_by(competency_id=competency_id).all()
        result = [
            {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "platform": course.platform,
                "url": course.url,
            }
            for course in courses
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
