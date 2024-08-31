import frappe
import datetime

def patient_update(doc, method=None):
    patients = frappe.db.get_list('Patient', fields=['*'], order_by='name')
    frappe.publish_realtime("patients_updated", patients)

def patient_appointment_inserted(doc, method=None):
    if doc.status == 'Walked In':
        doc.custom_visit_status = 'Arrived'
        doc.append("custom_appointment_time_logs", {
            "status": 'Arrived',
            "time": datetime.datetime.now()
        })
        doc.save()

def patient_encounter_inserted(doc, method=None):
    if doc.appointment:
        appointment = frappe.get_doc('Patient Appointment', doc.appointment)
        appointment.custom_visit_status = 'In Room'
        appointment.append("custom_appointment_time_logs", {
            "status": 'In Room',
            "time": datetime.datetime.now()
        })
        appointment.save()

def patient_encounter_update(doc, method=None):
    encounters = frappe.db.get_list('Patient Encounter', fields=['*'], order_by='name')
    frappe.publish_realtime("patient_encounters_updated", encounters)

def patient_encounter_submit(doc, method=None):
    if doc.appointment:
        appointment = frappe.get_doc('Patient Appointment', doc.appointment)
        appointment.custom_visit_status = 'Completed'
        appointment.append("custom_appointment_time_logs", {
            "status": 'Completed',
            "time": datetime.datetime.now()
        })
        appointment.save()