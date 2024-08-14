from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Patient(db.Model):

    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    patient_email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    patient_name = db.Column(db.String)
    gender = db.Column(db.String)
    insurance = db.Column(db.String)
    allergies = db.Column(db.String)
    medications = db.Column(db.String)

    def __repr__(self):
        return f'<Patient patient_id={self.patient_id} email={self.patient_email} name={self.patient_name} >'
    
class Doctor(db.Model):

    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    doctor_name = db.Column(db.String)
    availability = db.Column(db.String)
    specialty = db.Column(db.String)
    doctor_email = db.Column(db.String, unique = True)
    address = db.Column(db.String)

    def __repr__(self):
        return f'<Doctor doctor_id={self.doctor_id} email={self.email} name={self.name} specialty={self.specialty} >'
    
class Appointment(db.Model):

    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    visit_date = db.Column(db.Date)
    visit_time = db.Column(db.Time)
    reason = db.Column(db.Text)
    notes = db.Column(db.String)
    location = db.Column(db.String)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"))

    doctor = db.relationship("Doctor", backref="appointments")
    patient = db.relationship("Patient", backref="appointments")

    def __repr__(self):
        return f'<Appointments appt_id={self.appt_id} visit_date={self.visit_date} reason={self.reason} location={self.location} >'
    
def connect_to_db(flask_app, db_uri="postgresql://postgres:1982@localhost:5432/careflow", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)