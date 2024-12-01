from flask import Blueprint, request, jsonify
from database import db
from models import Project, Employee

project_blueprint = Blueprint('projects', __name__)

@project_blueprint.route('/', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'GET':
        projects = Project.query.all()
        result = [
            {
                "id": proj.id,
                "name": proj.name,
                "description": proj.description,
                "required_skills": proj.required_skills,
                "timeline": proj.timeline,
                "manager_id": proj.manager_id
            } for proj in projects
        ]
        return jsonify(result), 200

    if request.method == 'POST':
        data = request.get_json()
        new_project = Project(
            name=data['name'],
            description=data['description'],
            required_skills=data['required_skills'],
            timeline=data['timeline'],
            manager_id=data['manager_id']
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify({"message": "Project created successfully"}), 201

@project_blueprint.route('/match/<int:employee_id>', methods=['GET'])
def match_projects(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee_skills = set(employee.skills.split(', '))
    projects = Project.query.all()

    matched_projects = []
    for proj in projects:
        required_skills = set(proj.required_skills.split(', '))
        match_percentage = len(employee_skills & required_skills) / len(required_skills) * 100
        matched_projects.append({
            "project_id": proj.id,
            "name": proj.name,
            "match_percentage": match_percentage
        })

    return jsonify(matched_projects), 200
