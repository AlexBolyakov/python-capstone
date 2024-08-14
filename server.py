
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

    appt = crud.get_appointments()

    return render_template("all_appointments.html", appt=appt)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)