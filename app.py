from flask import Flask
from flask_cors import CORS
from database import db
from routes.employees import employee_blueprint
from routes.projects import project_blueprint
from routes.training import training_blueprint
from routes.feedback import feedback_blueprint
from routes.competencies import competencies_blueprint
from routes.leaves import leave_blueprint
from routes.certifications import certifications_blueprint
from routes.scheduler import start_scheduler
from routes.auth import auth_blueprint 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Swap%40123@localhost/aoi_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(employee_blueprint, url_prefix='/api/employees')
app.register_blueprint(project_blueprint, url_prefix='/api/projects')
app.register_blueprint(training_blueprint, url_prefix='/api/training')
app.register_blueprint(feedback_blueprint, url_prefix='/api/feedback')
app.register_blueprint(competencies_blueprint, url_prefix='/api/competencies')
app.register_blueprint(leave_blueprint, url_prefix='/api/leaves')
app.register_blueprint(certifications_blueprint, url_prefix='/api/certifications')
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')


# Error handling
@app.errorhandler(404)
def not_found_error(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "An internal error occurred"}, 500

# Start the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables in the database
    start_scheduler()  # Start the APScheduler
    app.run(debug=True)
