import frappe

def patient_update(*args):
    patients = frappe.db.get_list('Patient', fields=['*'], order_by='name')
    frappe.publish_realtime("patients_updated", patients)

def patient_encounter_update(*args):
    encounters = frappe.db.get_list('Patient Encounter', fields=['*'], order_by='name')
    frappe.publish_realtime("patient_encounters_updated", encounters)