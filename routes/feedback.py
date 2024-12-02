from flask import Blueprint, request, jsonify
from database import db
from models import Feedback, Employee, User

feedback_blueprint = Blueprint('feedback', __name__)

# Get feedback for a specific employee
@feedback_blueprint.route('/<int:employee_id>', methods=['GET'])
def get_feedback(employee_id):
    try:
        feedbacks = Feedback.query.filter_by(employee_id=employee_id).all()
        result = [
            {
                "id": fb.id,
                "comments": fb.comments,
                "sentiment": fb.sentiment
            } for fb in feedbacks
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add new feedback
@feedback_blueprint.route('/', methods=['POST'])
def add_feedback():
    data = request.get_json()
    try:
        new_feedback = Feedback(
            employee_id=data['employee_id'],
            manager_id=data['manager_id'],
            comments=data['comments'],
            sentiment=data.get('sentiment', 'Neutral')
        )
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({"message": "Feedback added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Get employees with feedback for a specific manager
@feedback_blueprint.route('/manager/<int:manager_id>', methods=['GET'])
def get_employees_with_feedback(manager_id):
    try:
        employees = (
            db.session.query(
                Employee.id.label('employee_id'),
                Employee.name.label('employee_name'),
                Feedback.comments,
                Feedback.sentiment
            )
            .outerjoin(Feedback, Feedback.employee_id == Employee.id)
            .filter(Employee.manager_id == manager_id)
            .all()
        )

        result = {}
        for emp in employees:
            if emp.employee_id not in result:
                result[emp.employee_id] = {
                    "employee_name": emp.employee_name,
                    "feedbacks": []
                }
            if emp.comments:
                result[emp.employee_id]["feedbacks"].append({
                    "comments": emp.comments,
                    "sentiment": emp.sentiment
                })

        return jsonify(list(result.values())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get all feedback with employee and manager details (HR functionality)
@feedback_blueprint.route('/hr', methods=['GET'])
def get_all_feedback():
    try:
        feedbacks = (
            db.session.query(
                Feedback.id,
                Feedback.comments,
                Feedback.sentiment,
                Employee.name.label('employee_name'),
                User.username.label('manager_name')
            )
            .join(Employee, Feedback.employee_id == Employee.id)
            .join(User, Feedback.manager_id == User.id)
            .all()
        )

        result = [
            {
                "id": fb.id,
                "employee_name": fb.employee_name,
                "manager_name": fb.manager_name,
                "comments": fb.comments,
                "sentiment": fb.sentiment,
            }
            for fb in feedbacks
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
