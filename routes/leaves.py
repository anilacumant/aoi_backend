from flask import Blueprint, request, jsonify
from database import db
from models import Leave, Employee
from datetime import datetime

leave_blueprint = Blueprint('leaves', __name__)

# Add a new leave request
@leave_blueprint.route('/apply', methods=['POST'])
def apply_leave():
    try:
        data = request.get_json()
        required_fields = ['employee_id', 'start_date', 'end_date', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        if start_date > end_date:
            return jsonify({"error": "start_date must be before or equal to end_date"}), 400

        new_leave = Leave(
            employee_id=data['employee_id'],
            start_date=start_date,
            end_date=end_date,
            type=data['type'],
            status='Pending'
        )
        db.session.add(new_leave)
        db.session.commit()
        return jsonify({"message": "Leave request submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all leave requests for a specific manager
@leave_blueprint.route('/manager/<int:manager_id>', methods=['GET'])
def get_manager_leaves(manager_id):
    try:
        employees = Employee.query.filter_by(manager_id=manager_id).all()
        employee_ids = [emp.id for emp in employees]
        leaves = Leave.query.filter(Leave.employee_id.in_(employee_ids)).all()
        result = [
            {
                "id": leave.id,
                "employee_id": leave.employee_id,
                "employee_name": leave.employee.name,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "type": leave.type,
                "status": leave.status
            } for leave in leaves
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Approve or reject a leave request
@leave_blueprint.route('/update/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    try:
        data = request.get_json()
        if 'status' not in data or data['status'] not in ['Approved', 'Rejected']:
            return jsonify({"error": "Valid 'status' is required ('Approved' or 'Rejected')"}), 400

        leave = Leave.query.get_or_404(leave_id)
        leave.status = data['status']
        db.session.commit()
        return jsonify({"message": "Leave status updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get leave history for an employee
@leave_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_leaves(employee_id):
    try:
        leaves = Leave.query.filter_by(employee_id=employee_id).all()
        result = [
            {
                "id": leave.id,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "type": leave.type,
                "status": leave.status
            } for leave in leaves
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
