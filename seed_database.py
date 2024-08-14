import os
import json
from datetime import datetime

import crud
import model
import server
from server import app

os.system("psql -U postgres -c\"drop database careflow\"")
os.system("psql -U postgres -c\"create database careflow\"")

model.connect_to_db(server.app)
with app.app_context():

    model.db.create_all()

    with open("data/patients.json") as f:
        patient_data = json.loads(f.read())

        patients_in_db = []
        for patient in patient_data:
            patient_email, password, patient_name, gender, insurance, allergies, medications = (
                patient["patient_email"],
                patient["password"],
                patient["patient_name"],
                patient["gender"],
                patient["insurance"],
                patient["allergies"],
                patient["medications"]
            )
            db_patient = crud.create_patient(patient_email, password, patient_name, gender, insurance, allergies, medications)
            patients_in_db.append(db_patient)
        
        model.db.session.add_all(patients_in_db)
        model.db.session.commit()
    
    with open("data/doctors.json") as f:
        doctor_data = json.loads(f.read())

        doctors_in_db = []
        for doctor in doctor_data:
            doctor_name, availability, specialty, doctor_email, address = (
                doctor["doctor_name"],
                doctor["availability"],
                doctor["specialty"],
                doctor["doctor_email"],
                doctor["address"]
            )
            db_doctor = crud.create_doctor(doctor_name, availability, specialty, doctor_email, address)
            doctors_in_db.append(db_doctor)

        model.db.session.add_all(doctors_in_db)
        model.db.session.commit()
   

    with open("data/appointments.json") as f:
        appt_data = json.loads(f.read())
        print(appt_data)

        appt_in_db = []
        for appt in appt_data:
            visit_date, visit_time, reason, notes, location, doctor_id, patient_id = (
                appt["visit_date"],
                appt["visit_time"],
                appt["reason"],
                appt["notes"],
                appt["location"],
                int(appt["doctor_id"]),
                int(appt["patient_id"])
            )

            doctor = model.Doctor.query.get(doctor_id)
            patient = model.Patient.query.get(patient_id)

            if doctor and patient:
                db_appt = crud.create_appt(visit_date, visit_time, reason, notes, location, doctor, patient)
                appt_in_db.append(db_appt)
            else:
                print(f"Skipping appointment with doctor_id={doctor_id} or patient_id={patient_id} because of missing records")
        
        model.db.session.add_all(appt_in_db)
        model.db.session.commit()


