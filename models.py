from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('HR', 'Manager', 'Employee'), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text)
    certifications = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL', onupdate='CASCADE'))

class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department = db.Column(db.String(100))

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    timeline = db.Column(db.String(50))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

class EmployeeProject(db.Model):
    __tablename__ = 'employee_projects'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    status = db.Column(db.Enum('Applied', 'Assigned', 'Completed'), default='Applied')

class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    program_name = db.Column(db.String(100))
    status = db.Column(db.Enum('In-progress', 'Completed'), default='In-progress')

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    comments = db.Column(db.Text)
    sentiment = db.Column(db.Enum('Positive', 'Negative', 'Neutral'))
    

class EmployeeCompetency(db.Model):
    __tablename__ = 'employee_competencies'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'), nullable=False)
    status = db.Column(db.Enum('Not Started', 'In Progress', 'Completed'), default='Not Started')

    competency = db.relationship('Competency')

class RoleCompetency(db.Model):
    __tablename__ = 'role_competencies'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'), nullable=False)

    competency = db.relationship('Competency')

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    platform = db.Column(db.Enum('Free', 'Paid'), nullable=False)
    url = db.Column(db.Text)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'))
    
class CertificationRequest(db.Model):
    __tablename__ = 'certification_requests'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    certification_name = db.Column(db.String(255), nullable=False)
    requested_date = db.Column(db.Date, nullable=False)
    approval_status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending')
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class Competency(db.Model):
    __tablename__ = 'competencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum('Skill', 'Certification', 'Training'), nullable=False)
    expiry_date = db.Column(db.Date)
    notification_sent = db.Column(db.Boolean, default=False)

class Leave(db.Model):
    __tablename__ = 'leaves'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.Enum('Sick', 'Vacation', 'Other'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending')

    # Relationship with Employee
    employee = db.relationship('Employee', backref='leaves')

    def __repr__(self):
        return f"<Leave(id={self.id}, employee_id={self.employee_id}, type={self.type}, status={self.status})>"

    

class LearningResource(db.Model):
    __tablename__ = 'learning_resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('Course', 'Mentor', 'Project'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    competency_id = db.Column(db.Integer, db.ForeignKey('competencies.id'), nullable=True)

    # Define relationship if needed
    competency = db.relationship('Competency', backref='learning_resources', lazy=True)


class EmployeeLearning(db.Model):
    __tablename__ = 'employee_learning'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('learning_resources.id'), nullable=False)
    progress = db.Column(db.Enum('Not Started', 'In Progress', 'Completed'), default='Not Started')

    # Define relationships if needed
    employee = db.relationship('Employee', backref='learning_records', lazy=True)
    resource = db.relationship('LearningResource', backref='employee_records', lazy=True)


