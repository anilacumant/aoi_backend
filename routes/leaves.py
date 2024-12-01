from flask import Blueprint, request, jsonify
from database import db
from models import Leave, Employee

leave_blueprint = Blueprint('leaves', __name__)

# Add a new leave request
@leave_blueprint.route('/apply', methods=['POST'])
def apply_leave():
    data = request.get_json()
    new_leave = Leave(
        employee_id=data['employee_id'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        type=data['type'],
        status='Pending'
    )
    db.session.add(new_leave)
    db.session.commit()
    return jsonify({"message": "Leave request submitted successfully"}), 201

# Get all leave requests for a specific manager
@leave_blueprint.route('/manager/<int:manager_id>', methods=['GET'])
def get_manager_leaves(manager_id):
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

# Approve or reject a leave request
@leave_blueprint.route('/update/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json()
    leave = Leave.query.get_or_404(leave_id)
    leave.status = data['status']  # 'Approved' or 'Rejected'
    db.session.commit()
    return jsonify({"message": "Leave status updated successfully"}), 200

# Get all pending leave requests (for HR)
@leave_blueprint.route('/pending', methods=['GET'])
def get_pending_leaves():
    leaves = Leave.query.filter_by(status='Pending').all()
    result = [
        {
            "id": leave.id,
            "employee_id": leave.employee_id,
            "employee_name": leave.employee.name,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "type": leave.type
        } for leave in leaves
    ]
    return jsonify(result), 200

# Get leave history for an employee
@leave_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_leaves(employee_id):
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
