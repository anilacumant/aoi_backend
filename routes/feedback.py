from flask import Blueprint, request, jsonify
from database import db
from models import Feedback

feedback_blueprint = Blueprint('feedback', __name__)

@feedback_blueprint.route('/<int:employee_id>', methods=['GET'])
def get_feedback(employee_id):
    feedbacks = Feedback.query.filter_by(employee_id=employee_id).all()
    result = [
        {
            "id": fb.id,
            "comments": fb.comments,
            "sentiment": fb.sentiment
        } for fb in feedbacks
    ]
    return jsonify(result), 200

@feedback_blueprint.route('/', methods=['POST'])
def add_feedback():
    data = request.get_json()
    new_feedback = Feedback(
        employee_id=data['employee_id'],
        manager_id=data['manager_id'],
        comments=data['comments'],
        sentiment=data.get('sentiment', 'Neutral')
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({"message": "Feedback added successfully"}), 201
