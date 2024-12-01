from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
from database import db
from models import Competency, Employee, User

def check_certification_expiry():
    with current_app.app_context():
        today = datetime.today()
        near_expiry_date = today + timedelta(days=30)  # 30-day notification window

        # Find certifications nearing expiry
        certifications = Competency.query.filter(
            Competency.expiry_date <= near_expiry_date,
            Competency.notification_sent == False
        ).all()

        for cert in certifications:
            # Notify the manager and employee
            employee_competencies = cert.employeecompetency_set  # Access linked employees
            for emp_comp in employee_competencies:
                employee = emp_comp.employee
                manager = User.query.get(employee.manager_id)

                # Example: Log or send email/notification (to be replaced with actual notification logic)
                print(f"Notify {manager.username}: Certification {cert.name} for {employee.name} expires on {cert.expiry_date}.")

            # Mark notification as sent
            cert.notification_sent = True
            db.session.commit()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_certification_expiry, 'interval', hours=24)  # Runs daily
    scheduler.start()
