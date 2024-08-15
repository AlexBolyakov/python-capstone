
from model import db, Patient, Doctor, Appointment, connect_to_db

def create_patient(patient_email, password, patient_name, gender, insurance, allergies, medications):
    
    patient = Patient(patient_email=patient_email, password=password, patient_name=patient_name, gender=gender, insurance=insurance, allergies=allergies, medications=medications)

    return patient


def create_doctor(doctor_name, availability, specialty, doctor_email, address):

    doctor = Doctor(doctor_name=doctor_name, availability=availability, specialty=specialty, doctor_email=doctor_email, address=address)

    return doctor


def create_appt(visit_date, visit_time, reason, notes, location, doctor, patient):
    
    if not isinstance(doctor, Doctor) or not isinstance(patient, Patient):
        raise ValueError("doctor and patient must be instances of Doctor and Patient respectively")

    appt = Appointment(visit_date=visit_date, visit_time=visit_time, reason=reason, notes=notes, location=location, doctor=doctor, patient=patient)
    db.session.add(appt)
    db.session.commit()
    return appt

def get_patients():

    return Patient.query.all()

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)

def get_doctors():

    return Doctor.query.all()

def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)

def get_appointments():
    appointments = Appointment.query.all()
    # print(appointments)
    appointments = Appointment.query.all()
    results = []

    for appointment in appointments:
        appointment_info = {
            'appointment_id': appointment.appt_id,
            'visit_date': appointment.visit_date,
            'visit_time': appointment.visit_time,
            'reason': appointment.reason,
            'notes': appointment.notes,
            'location': appointment.location,
            'doctor_name': appointment.doctor.doctor_name,
            'patient_name': appointment.patient.patient_name
        }
        results.append(appointment_info)

    return results
   
   
    # return f"Appointment with Doctor: {doctor_name}, MD, for Patient: {patient_name}"
       
def get_patient_by_email(patient_email):

    return Patient.query.filter(Patient.patient_email == patient_email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

