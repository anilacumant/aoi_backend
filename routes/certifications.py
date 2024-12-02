from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from database import db
from models import CertificationRequest, Competency, EmployeeCompetency, Employee, User

certifications_blueprint = Blueprint('certifications', __name__)

# Employee requests a new certification
@certifications_blueprint.route('/request', methods=['POST'])
def request_certification():
    try:
        data = request.get_json()
        new_request = CertificationRequest(
            employee_id=data['employee_id'],
            certification_name=data['certification_name'],
            requested_date=datetime.today(),
            manager_id=data['manager_id']
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message": "Certification request submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Manager views pending certification requests
@certifications_blueprint.route('/pending/<int:manager_id>', methods=['GET'])
def get_pending_requests(manager_id):
    try:
        requests = CertificationRequest.query.filter_by(manager_id=manager_id, approval_status='Pending').all()
        result = [
            {
                "id": req.id,
                "employee_id": req.employee_id,
                "certification_name": req.certification_name,
                "requested_date": req.requested_date,
                "approval_status": req.approval_status,
            } for req in requests
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Manager approves/rejects a certification request
@certifications_blueprint.route('/approve/<int:request_id>', methods=['PUT'])
def approve_certification(request_id):
    try:
        data = request.get_json()
        approval_status = data['approval_status']
        expiry_days = data.get('expiry_days', 365)  # Default expiry duration is 1 year

        cert_request = CertificationRequest.query.get_or_404(request_id)
        cert_request.approval_status = approval_status

        # If approved, add certification to the employee's competencies
        if approval_status == 'Approved':
            expiry_date = datetime.today() + timedelta(days=expiry_days)
            new_competency = Competency(
                name=cert_request.certification_name,
                description=f"Certification approved by Manager {cert_request.manager_id}",
                type='Certification',
                expiry_date=expiry_date
            )
            db.session.add(new_competency)
            db.session.flush()

            employee_competency = EmployeeCompetency(
                employee_id=cert_request.employee_id,
                competency_id=new_competency.id,
                status='Completed'
            )
            db.session.add(employee_competency)

        db.session.commit()
        return jsonify({"message": f"Certification request {approval_status.lower()} successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all certifications for an employee
@certifications_blueprint.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee_certifications(employee_id):
    try:
        competencies = EmployeeCompetency.query.filter_by(employee_id=employee_id).all()
        result = [
            {
                "competency_name": comp.competency.name,
                "type": comp.competency.type,
                "status": comp.status,
                "expiry_date": comp.competency.expiry_date,
                "description": comp.competency.description
            } for comp in competencies if comp.competency.type == 'Certification'
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HR views all certifications and employees
@certifications_blueprint.route('/hr/overview', methods=['GET'])
def get_all_certifications():
    try:
        certifications = (
            db.session.query(
                Employee.id.label("employee_id"),
                Employee.name.label("employee_name"),
                User.username.label("manager_name"),
                Competency.name.label("certification_name"),
                Competency.expiry_date.label("expiry_date"),
                EmployeeCompetency.status.label("certification_status"),
            )
            .join(EmployeeCompetency, Employee.id == EmployeeCompetency.employee_id)
            .join(Competency, EmployeeCompetency.competency_id == Competency.id)
            .join(User, Employee.manager_id == User.id)
            .filter(Competency.type == "Certification")
            .all()
        )

        result = [
            {
                "employee_id": row.employee_id,
                "employee_name": row.employee_name,
                "manager_name": row.manager_name,
                "certification_name": row.certification_name,
                "expiry_date": row.expiry_date,
                "certification_status": row.certification_status,
            }
            for row in certifications
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HR sends notification for updating certifications
@certifications_blueprint.route('/send-notification/<int:employee_id>', methods=['POST'])
def send_notification(employee_id):
    try:
        data = request.get_json()
        certification_name = data["certification_name"]

        print(f"Notification sent to Employee ID {employee_id} for updating certification: {certification_name}")

        return jsonify({"message": f"Notification sent to employee {employee_id} for certification '{certification_name}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
