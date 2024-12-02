from flask import Blueprint, jsonify
from models import User

users_blueprint = Blueprint('users', __name__)

# Fetch all managers
@users_blueprint.route('/managers/', methods=['GET'])
def get_managers():
    try:
        managers = User.query.filter_by(role='Manager').all()
        if not managers:
            print("No managers found in the database.")
        else:
            print("Managers fetched successfully:", [m.username for m in managers])
        result = [
            {
                "id": manager.id,
                "username": manager.username
            } for manager in managers
        ]
        return jsonify(result), 200
    except Exception as e:
        print("Error fetching managers:", e)
        return jsonify({"error": str(e)}), 500
