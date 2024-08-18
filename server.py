
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    
    return render_template('homepage.html')

@app.route("/patients")
def all_patients():

    patients = crud.get_patients()

    return render_template("all_patients.html", patients=patients)

@app.route("/patients/<patient_id>")
def show_patient(patient_id):

    patient = crud.get_patient_by_id(patient_id)

    return render_template("patient_details.html", patient=patient)

@app.route("/doctors")
def all_doctors():

    doctors = crud.get_doctors()

    return render_template("all_doctors.html", doctors=doctors)

@app.route("/doctors/<doctor_id>")
def show_doctor(doctor_id):

    doctor = crud.get_doctor_by_id(doctor_id)

    return render_template("doctor_details.html", doctor=doctor)

@app.route("/appointments")
def all_appointments():

    appointments = crud.get_appointments()

    return render_template("all_appointments.html", appointments=appointments)

@app.route("/appointments/<appointment_id>")
def show_appointment(appointment_id):

    appointment = crud.get_appointment_by_id(appointment_id)

    return render_template("appointment_details.html", appointment=appointment)

@app.route("/patients", methods=["POST"])
def register_patient():

    email = request.form.get("patient_email")
    password = request.form.get("password")
    patient_name = request.form.get("patient_name")
    gender = request.form.get("gender")
    insurance = request.form.get("insurance")
    allergies = request.form.get("allergies")
    medications = request.form.get("medications")

    if not all([email, password, patient_name, gender, insurance, allergies, medications]):
        flash("Data entry is missing. Please fill out all fields.")
        return redirect("/")

    patient = crud.get_patient_by_email(email)
    if patient:
        flash("Unable to create account with provided email. Try again!")
    else:
        patient = crud.create_patient(email, password, patient_name, gender, insurance, allergies, medications)
        db.session.add(patient)
        db.session.commit()
        flash("Patient account was created successfully! Please log in.")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def patient_login():
    
    email = request.form.get("patient_email")
    password = request.form.get("password")

    if not all([email, password]):
        flash("Data entry is missing. Please fill out all fields.")
        return redirect("/")

    patient = crud.get_patient_by_email(email)
    if patient and patient.password == password:
        session["patient_email"] = patient.patient_email
        flash(f"Welcome back, {patient.patient_email}!")
    else:
        flash("The email or password is incorrect.")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)