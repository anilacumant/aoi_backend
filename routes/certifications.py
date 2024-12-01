import datetime
from flask import Blueprint, request, jsonify
from database import db
from models import CertificationRequest

certifications_blueprint = Blueprint('certifications', __name__)

# Employee requests a new certification
@certifications_blueprint.route('/request', methods=['POST'])
def request_certification():
    data = request.get_json()
    new_request = CertificationRequest(
        employee_id=data['employee_id'],
        certification_name=data['certification_name'],
        requested_date=datetime.today(),
        manager_id=data['manager_id']
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Certification request submitted"}), 201

# Manager views pending requests
@certifications_blueprint.route('/pending/<int:manager_id>', methods=['GET'])
def get_pending_requests(manager_id):
    requests = CertificationRequest.query.filter_by(manager_id=manager_id, approval_status='Pending').all()
    result = [
        {
            "id": req.id,
            "employee_name": req.employee.name,
            "certification_name": req.certification_name,
            "requested_date": req.requested_date
        } for req in requests
    ]
    return jsonify(result), 200

# Manager approves/rejects a request
@certifications_blueprint.route('/approve/<int:request_id>', methods=['PUT'])
def approve_certification(request_id):
    data = request.get_json()
    cert_request = CertificationRequest.query.get_or_404(request_id)
    cert_request.approval_status = data['approval_status']
    db.session.commit()
    return jsonify({"message": "Certification request updated"}), 200
