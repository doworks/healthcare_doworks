import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def add_custom_fields():
    doctype = 'Your Doctype Name'
    fieldname = 'your_custom_fieldname'

    # Check if the custom field already exists
    if not frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': fieldname}):
        # Define your custom field
        custom_field = {
            'fieldname': fieldname,
            'label': 'Your Custom Field Label',
            'fieldtype': 'Data',  # Change to your desired field type
            'insert_after': 'another_fieldname',  # Fieldname after which you want to insert your custom field
            'reqd': 0,  # Set to 1 if the field is required
            'description': 'A description of your custom field',
            # Add any additional properties for your field
        }

        # Create the custom field
        create_custom_field(doctype, custom_field)

        frappe.db.commit()  # Commit the changes to the database

    for field in custom_fields:
        doctype = field.get('dt')
        fieldname = field.get('fieldname')

        # Check if the custom field already exists
        if not frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': fieldname}):
            # Create the custom field
            create_custom_field(doctype, field)

            frappe.db.commit()  # Commit the changes to the database

custom_fields = [
    {"name": "Clinical Procedure-custom_patient_consent_signature", "dt": "Clinical Procedure", "fieldname": "custom_patient_consent_signature", "label": "Patient Consent Signature", "fieldtype": "Attach Image"}, 
    {"name": "Clinical Procedure-custom_patient_encounter", "dt": "Clinical Procedure", "fieldname": "custom_patient_encounter", "label": "Patient Encounter", "fieldtype": "Link"}, 
    {"name": "Clinical Procedure-custom_post_operative_diagnosis", "dt": "Clinical Procedure", "fieldname": "custom_post_operative_diagnosis", "label": "Post Operative Diagnosis", "fieldtype": "Small Text"}, 
    {"name": "Clinical Procedure-custom_pre_operative_diagnosis", "dt": "Clinical Procedure", "fieldname": "custom_pre_operative_diagnosis", "label": "Pre Operative Diagnosis", "fieldtype": "Small Text"}, 
    {"name": "Patient-custom_allergies_table", "dt": "Patient", "fieldname": "custom_allergies_table", "label": "Allergies Table", "fieldtype": "Table"}, 
    {"name": "Patient-custom_chronic_diseases", "dt": "Patient", "fieldname": "custom_chronic_diseases", "label": "Chronic Diseases", "fieldtype": "Small Text"}, 
    {"name": "Patient-custom_column_break_napf0", "dt": "Patient", "fieldname": "custom_column_break_napf0", "label": None, "fieldtype": "Column Break"}, 
    {"name": "Patient-custom_cpr", "dt": "Patient", "fieldname": "custom_cpr", "label": "CPR", "fieldtype": "Data"}, 
    {"name": "Patient-custom_family_history", "dt": "Patient", "fieldname": "custom_family_history", "label": "Family History", "fieldtype": "Section Break"}, 
    {"name": "Patient-custom_file_number", "dt": "Patient", "fieldname": "custom_file_number", "label": "File Number", "fieldtype": "Data"}, 
    {"name": "Patient-custom_genetic_conditions", "dt": "Patient", "fieldname": "custom_genetic_conditions", "label": "Genetic Conditions", "fieldtype": "Small Text"}, 
    {"name": "Patient-custom_habits__social", "dt": "Patient", "fieldname": "custom_habits__social", "label": "Habits / Social", "fieldtype": "Table"}, 
    {"name": "Patient-custom_infected_diseases", "dt": "Patient", "fieldname": "custom_infected_diseases", "label": "Infected Diseases", "fieldtype": "Table"}, 
    {"name": "Patient-custom_medications", "dt": "Patient", "fieldname": "custom_medications", "label": "Medications", "fieldtype": "Table"}, 
    {"name": "Patient-custom_risk_factors_table", "dt": "Patient", "fieldname": "custom_risk_factors_table", "label": "Risk Factors Table", "fieldtype": "Table"}, 
    {"name": "Patient-custom_surgical_history_table", "dt": "Patient", "fieldname": "custom_surgical_history_table", "label": "Surgical History Table", "fieldtype": "Table"}, 
    {"name": "Patient Appointment-custom_appointment_category", "dt": "Patient Appointment", "fieldname": "custom_appointment_category", "label": "Appointment Category", "fieldtype": "Select"}, 
    {"name": "Patient Appointment-custom_appointment_time_logs", "dt": "Patient Appointment", "fieldname": "custom_appointment_time_logs", "label": "Appointment Time Logs", "fieldtype": "Table"}, 
    {"name": "Patient Appointment-custom_confirmed", "dt": "Patient Appointment", "fieldname": "custom_confirmed", "label": "Confirmed", "fieldtype": "Check"}, 
    {"name": "Patient Appointment-custom_past_appointment", "dt": "Patient Appointment", "fieldname": "custom_past_appointment", "label": "Past Appointment", "fieldtype": "Link"}, 
    {"name": "Patient Appointment-custom_payment_type", "dt": "Patient Appointment", "fieldname": "custom_payment_type", "label": "Payment Type", "fieldtype": "Select"}, 
    {"name": "Patient Appointment-custom_visit_notes", "dt": "Patient Appointment", "fieldname": "custom_visit_notes", "label": "Visit Notes", "fieldtype": "Table"}, 
    {"name": "Patient Appointment-custom_visit_reason", "dt": "Patient Appointment", "fieldname": "custom_visit_reason", "label": "Visit Reason", "fieldtype": "Data"}, 
    {"name": "Patient Appointment-custom_visit_status", "dt": "Patient Appointment", "fieldname": "custom_visit_status", "label": "Visit Status", "fieldtype": "Select"}, 
    {"name": "Patient Encounter-custom_appointment_category", "dt": "Patient Encounter", "fieldname": "custom_appointment_category", "label": "Appointment Category", "fieldtype": "Data"}, 
    {"name": "Patient Encounter-custom_attachments", "dt": "Patient Encounter", "fieldname": "custom_attachments", "label": "Attachments", "fieldtype": "Table"}, 
    {"name": "Patient Encounter-custom_diagnosis_note", "dt": "Patient Encounter", "fieldname": "custom_diagnosis_note", "label": "Diagnosis Note", "fieldtype": "Small Text"}, 
    {"name": "Patient Encounter-custom_differential_diagnosis", "dt": "Patient Encounter", "fieldname": "custom_differential_diagnosis", "label": "Differential Diagnosis", "fieldtype": "Table MultiSelect"}, 
    {"name": "Patient Encounter-custom_encounter_start_time", "dt": "Patient Encounter", "fieldname": "custom_encounter_start_time", "label": "Encounter Start Time", "fieldtype": "Datetime"}, 
    {"name": "Patient Encounter-custom_encounter_state", "dt": "Patient Encounter", "fieldname": "custom_encounter_state", "label": "Encounter State", "fieldtype": "Select"}, 
    {"name": "Patient Encounter-custom_illness_progression", "dt": "Patient Encounter", "fieldname": "custom_illness_progression", "label": "Illness Progression", "fieldtype": "Small Text"}, 
    {"name": "Patient Encounter-custom_illness_progression_section", "dt": "Patient Encounter", "fieldname": "custom_illness_progression_section", "label": "Illness Progression", "fieldtype": "Section Break"}, 
    {"name": "Patient Encounter-custom_other_examination", "dt": "Patient Encounter", "fieldname": "custom_other_examination", "label": "Other Examination", "fieldtype": "Small Text"}, 
    {"name": "Patient Encounter-custom_physical_examination", "dt": "Patient Encounter", "fieldname": "custom_physical_examination", "label": "Physical Examination", "fieldtype": "Small Text"}, 
    {"name": "Patient Encounter-custom_section_break_w6rwb", "dt": "Patient Encounter", "fieldname": "custom_section_break_w6rwb", "label": "", "fieldtype": "Section Break"}, 
    {"name": "Patient Encounter-custom_symptoms_duration", "dt": "Patient Encounter", "fieldname": "custom_symptoms_duration", "label": "Symptoms Duration", "fieldtype": "Int"}, 
    {"name": "Patient Encounter-custom_symptoms_notes", "dt": "Patient Encounter", "fieldname": "custom_symptoms_notes", "label": "Symptoms Notes", "fieldtype": "Small Text"}, 
]