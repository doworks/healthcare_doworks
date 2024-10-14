import frappe

def get_custom_fields_in_healthcare():
    # Get all DocTypes that belong to the Healthcare module
    healthcare_doctypes = frappe.get_all(
        'DocType',
        filters={'module': 'Healthcare'},
        fields=['name']
    )

    # Extract the names of the DocTypes
    healthcare_doctype_names = [doctype['name'] for doctype in healthcare_doctypes]

    # Retrieve custom fields for these DocTypes
    custom_fields = frappe.get_all(
        'Custom Field',
        filters={'dt': ['in', healthcare_doctype_names]},
        fields=['name', 'dt', 'fieldname', 'label', 'fieldtype', 'creation', 'reqd', 'insert_after', 'description', 'options'],
        order_by='dt, creation desc'
    )

    # Print details of each custom field
    for field in custom_fields:
        print(f"Doctype: {field['dt']}, Fieldname: {field['fieldname']}, Label: {field['label']}, Fieldtype: {field['fieldtype']}, Created on: {field['creation']}")

    return custom_fields

if __name__ == "__main__":
    custom_fields_in_healthcare = get_custom_fields_in_healthcare()


def add_custom_fields():
    """
    Ensure that each custom field in the list exists in the specified DocType.
    
    :param custom_fields_list: List of custom field definitions. Each definition is a dictionary.
    """
    for field in custom_fields:
        doctype = field.get('dt')
        fieldname = field.get('fieldname')

        # Check if the custom field already exists
        if not frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': fieldname}):
            # Create a new custom field
            custom_field = frappe.get_doc({
                'doctype': 'Custom Field',
                'dt': doctype,
                'fieldname': fieldname,
                'label': field.get('label', ''),
                'fieldtype': field.get('fieldtype', 'Data'),
                'insert_after': field.get('insert_after', ''),
                'reqd': field.get('reqd', 0),
                'description': field.get('description', ''),
                'options': field.get('options', ''),
                'creation': field.get('creation', ''),
                # Add any additional properties here
            })
            custom_field.insert()
            frappe.db.commit()  # Commit the changes to the database

custom_fields = [{"name": "Clinical Procedure-custom_general_data", "dt": "Clinical Procedure", "fieldname": "custom_general_data", "label": "General Data", "fieldtype": "Text Editor", "creation": "2024-10-13 11:31:41.906756", "reqd": 0, "insert_after": "custom_procedure", "description": None, "options": None}, {"name": "Clinical Procedure-custom_procedure", "dt": "Clinical Procedure", "fieldname": "custom_procedure", "label": "Procedure", "fieldtype": "Section Break", "creation": "2024-10-13 11:31:41.691353", "reqd": 0, "insert_after": "custom_patient_consent_signature", "description": None, "options": None}, {"name": "Clinical Procedure-custom_annotations", "dt": "Clinical Procedure", "fieldname": "custom_annotations", "label": "Annotations", "fieldtype": "Table", "creation": "2024-08-11 14:32:42.873720", "reqd": 0, "insert_after": "custom_annotations_section", "description": None, "options": "Health Annotation Table"}, {"name": "Clinical Procedure-custom_annotations_section", "dt": "Clinical Procedure", "fieldname": "custom_annotations_section", "label": "Annotations", "fieldtype": "Section Break", "creation": "2024-08-11 14:32:42.742985", "reqd": 0, "insert_after": "custom_general_data", "description": None, "options": None}, {"name": "Clinical Procedure-custom_patient_consent_signature", "dt": "Clinical Procedure", "fieldname": "custom_patient_consent_signature", "label": "Patient Consent Signature", "fieldtype": "Attach Image", "creation": "2024-08-08 11:38:57.168985", "reqd": 0, "insert_after": "sample", "description": None, "options": None}, {"name": "Clinical Procedure-custom_post_operative_diagnosis", "dt": "Clinical Procedure", "fieldname": "custom_post_operative_diagnosis", "label": "Post Operative Diagnosis", "fieldtype": "Small Text", "creation": "2024-08-07 13:05:30.487713", "reqd": 0, "insert_after": "custom_pre_operative_diagnosis", "description": None, "options": None}, {"name": "Clinical Procedure-custom_pre_operative_diagnosis", "dt": "Clinical Procedure", "fieldname": "custom_pre_operative_diagnosis", "label": "Pre Operative Diagnosis", "fieldtype": "Small Text", "creation": "2024-08-07 13:05:30.312677", "reqd": 0, "insert_after": "notes", "description": None, "options": None}, {"name": "Clinical Procedure-custom_patient_encounter", "dt": "Clinical Procedure", "fieldname": "custom_patient_encounter", "label": "Patient Encounter", "fieldtype": "Link", "creation": "2024-08-07 09:56:04.418867", "reqd": 0, "insert_after": "appointment", "description": None, "options": "Patient Encounter"}, {"name": "Medication Request-auto_repeat", "dt": "Medication Request", "fieldname": "auto_repeat", "label": "Auto Repeat", "fieldtype": "Link", "creation": "2024-05-17 22:25:15.824547", "reqd": 0, "insert_after": "amended_from", "description": None, "options": "Auto Repeat"}, {"name": "Patient-custom_insurance_company_name", "dt": "Patient", "fieldname": "custom_insurance_company_name", "label": "Insurance Company Name", "fieldtype": "Link", "creation": "2024-09-23 12:22:40.974459", "reqd": 0, "insert_after": "custom_active", "description": None, "options": "Customer"}, {"name": "Patient-custom_default_payment_type", "dt": "Patient", "fieldname": "custom_default_payment_type", "label": "Default Payment Type", "fieldtype": "Select", "creation": "2024-09-23 10:56:25.380580", "reqd": 0, "insert_after": "custom_medical_history_last_updated", "description": None, "options": "Self Payment\nInsurance"}, {"name": "Patient-custom_copay_amount", "dt": "Patient", "fieldname": "custom_copay_amount", "label": "Copay Amount", "fieldtype": "Float", "creation": "2024-09-23 10:12:39.744604", "reqd": 0, "insert_after": "custom_expiration_date", "description": None, "options": None}, {"name": "Patient-custom_active", "dt": "Patient", "fieldname": "custom_active", "label": "Active", "fieldtype": "Check", "creation": "2024-09-23 10:12:39.624564", "reqd": 0, "insert_after": "custom_insurance", "description": None, "options": None}, {"name": "Patient-custom_expiration_date", "dt": "Patient", "fieldname": "custom_expiration_date", "label": "Expiration Date", "fieldtype": "Date", "creation": "2024-09-23 10:12:39.507888", "reqd": 0, "insert_after": "custom_policy_number", "description": None, "options": None}, {"name": "Patient-custom_policy_number", "dt": "Patient", "fieldname": "custom_policy_number", "label": "Policy Number", "fieldtype": "Data", "creation": "2024-09-23 10:12:39.378514", "reqd": 0, "insert_after": "custom_insurance_company_name", "description": None, "options": None}, {"name": "Patient-custom_insurance", "dt": "Patient", "fieldname": "custom_insurance", "label": "Insurance", "fieldtype": "Tab Break", "creation": "2024-09-23 10:12:39.118216", "reqd": 0, "insert_after": "other_risk_factors", "description": None, "options": None}, {"name": "Patient-custom_medical_history_last_updated", "dt": "Patient", "fieldname": "custom_medical_history_last_updated", "label": "Medical History Last Updated", "fieldtype": "Date", "creation": "2024-08-11 11:27:14.738469", "reqd": 0, "insert_after": "patient_details", "description": None, "options": None}, {"name": "Patient-custom_infected_diseases", "dt": "Patient", "fieldname": "custom_infected_diseases", "label": "Infected Diseases", "fieldtype": "Table", "creation": "2024-05-13 11:29:03.807932", "reqd": 0, "insert_after": "surgical_history", "description": None, "options": "Infected Diseases Table"}, {"name": "Patient-custom_medications", "dt": "Patient", "fieldname": "custom_medications", "label": "Medications", "fieldtype": "Table", "creation": "2024-05-11 14:57:00.679744", "reqd": 0, "insert_after": "custom_allergies_table", "description": None, "options": "Patient Medications Table"}, {"name": "Patient-custom_genetic_conditions", "dt": "Patient", "fieldname": "custom_genetic_conditions", "label": "Genetic Conditions", "fieldtype": "Small Text", "creation": "2024-05-11 14:57:00.570605", "reqd": 0, "insert_after": "custom_column_break_napf0", "description": None, "options": None}, {"name": "Patient-custom_column_break_napf0", "dt": "Patient", "fieldname": "custom_column_break_napf0", "label": None, "fieldtype": "Column Break", "creation": "2024-05-11 14:57:00.480783", "reqd": 0, "insert_after": "custom_chronic_diseases", "description": None, "options": None}, {"name": "Patient-custom_chronic_diseases", "dt": "Patient", "fieldname": "custom_chronic_diseases", "label": "Chronic Diseases", "fieldtype": "Small Text", "creation": "2024-05-11 14:57:00.355674", "reqd": 0, "insert_after": "custom_family_history", "description": None, "options": None}, {"name": "Patient-custom_family_history", "dt": "Patient", "fieldname": "custom_family_history", "label": "Family History", "fieldtype": "Section Break", "creation": "2024-05-11 14:57:00.212258", "reqd": 0, "insert_after": "marital_status", "description": None, "options": None}, {"name": "Patient-custom_habits__social", "dt": "Patient", "fieldname": "custom_habits__social", "label": "Habits / Social", "fieldtype": "Table", "creation": "2024-05-11 14:57:00.029140", "reqd": 0, "insert_after": "occupation", "description": None, "options": "Patient Habits Table"}, {"name": "Patient-custom_file_number", "dt": "Patient", "fieldname": "custom_file_number", "label": "File Number", "fieldtype": "Data", "creation": "2024-05-08 10:17:53.812771", "reqd": 0, "insert_after": "user_id", "description": None, "options": None}, {"name": "Patient-custom_risk_factors_table", "dt": "Patient", "fieldname": "custom_risk_factors_table", "label": "Risk Factors Table", "fieldtype": "Table", "creation": "2024-05-01 18:55:03.512129", "reqd": 0, "insert_after": "alcohol_current_use", "description": None, "options": "Patient Risk Factors"}, {"name": "Patient-custom_surgical_history_table", "dt": "Patient", "fieldname": "custom_surgical_history_table", "label": "Surgical History Table", "fieldtype": "Table", "creation": "2024-05-01 18:55:03.410595", "reqd": 0, "insert_after": "custom_infected_diseases", "description": None, "options": "Patient Surgical History"}, {"name": "Patient-custom_allergies_table", "dt": "Patient", "fieldname": "custom_allergies_table", "label": "Allergies Table", "fieldtype": "Table", "creation": "2024-05-01 18:55:03.298346", "reqd": 0, "insert_after": "medication", "description": None, "options": "Patient Allergies Table"}, {"name": "Patient-custom_cpr", "dt": "Patient", "fieldname": "custom_cpr", "label": "CPR", "fieldtype": "Data", "creation": "2024-04-07 18:06:48.618767", "reqd": 0, "insert_after": "patient_name", "description": None, "options": None}, {"name": "Patient Appointment-custom_procedure_templates", "dt": "Patient Appointment", "fieldname": "custom_procedure_templates", "label": "Procedure Templates", "fieldtype": "Table MultiSelect", "creation": "2024-10-02 13:22:46.587571", "reqd": 0, "insert_after": "custom_appointment_category", "description": None, "options": "Procedure Template Multi-select"}, {"name": "Patient Appointment-custom_customer", "dt": "Patient Appointment", "fieldname": "custom_customer", "label": "Customer", "fieldtype": "Data", "creation": "2024-09-21 09:04:22.163733", "reqd": 0, "insert_after": "patient_name", "description": None, "options": None}, {"name": "Patient Appointment-custom_invoice_items", "dt": "Patient Appointment", "fieldname": "custom_invoice_items", "label": "Invoice Items", "fieldtype": "Table", "creation": "2024-09-16 09:20:26.892762", "reqd": 0, "insert_after": "ref_sales_invoice", "description": None, "options": "Healthcare Invoice Item"}, {"name": "Patient Appointment-custom_branch", "dt": "Patient Appointment", "fieldname": "custom_branch", "label": "Branch", "fieldtype": "Link", "creation": "2024-09-04 09:42:27.967614", "reqd": 0, "insert_after": "company", "description": None, "options": "Branch"}, {"name": "Patient Appointment-custom_past_appointment", "dt": "Patient Appointment", "fieldname": "custom_past_appointment", "label": "Past Appointment", "fieldtype": "Link", "creation": "2024-08-06 09:46:13.714583", "reqd": 0, "insert_after": "custom_procedure_templates", "description": None, "options": "Patient Appointment"}, {"name": "Patient Appointment-custom_visit_reason", "dt": "Patient Appointment", "fieldname": "custom_visit_reason", "label": "Visit Reason", "fieldtype": "Data", "creation": "2024-05-08 11:55:04.202376", "reqd": 0, "insert_after": "appointment_for", "description": None, "options": None}, {"name": "Patient Appointment-custom_visit_notes", "dt": "Patient Appointment", "fieldname": "custom_visit_notes", "label": "Visit Notes", "fieldtype": "Table", "creation": "2024-04-07 21:50:31.737567", "reqd": 0, "insert_after": "notes", "description": None, "options": "Appointment Note Table"}, {"name": "Patient Appointment-custom_payment_type", "dt": "Patient Appointment", "fieldname": "custom_payment_type", "label": "Payment Type", "fieldtype": "Select", "creation": "2024-04-03 08:57:58.132050", "reqd": 0, "insert_after": "section_break_16", "description": None, "options": "\nSelf Payment\nInsurance"}, {"name": "Patient Appointment-custom_confirmed", "dt": "Patient Appointment", "fieldname": "custom_confirmed", "label": "Confirmed", "fieldtype": "Check", "creation": "2024-04-03 08:53:40.578532", "reqd": 0, "insert_after": "reminded", "description": None, "options": None}, {"name": "Patient Appointment-custom_appointment_time_logs", "dt": "Patient Appointment", "fieldname": "custom_appointment_time_logs", "label": "Appointment Time Logs", "fieldtype": "Table", "creation": "2024-04-03 08:21:46.688221", "reqd": 0, "insert_after": "custom_visit_status", "description": None, "options": "Appointment Time Logs"}, {"name": "Patient Appointment-custom_appointment_category", "dt": "Patient Appointment", "fieldname": "custom_appointment_category", "label": "Appointment Category", "fieldtype": "Select", "creation": "2024-04-03 07:52:23.344612", "reqd": 0, "insert_after": "custom_appointment_time_logs", "description": None, "options": "First Time\nFollow-up\nProcedure\nSession"}, {"name": "Patient Appointment-custom_visit_status", "dt": "Patient Appointment", "fieldname": "custom_visit_status", "label": "Visit Status", "fieldtype": "Select", "creation": "2024-04-02 15:30:57.843283", "reqd": 0, "insert_after": "status", "description": None, "options": "Scheduled\nNo Show\nArrived\nReady\nIn Room\nTransferred\nCompleted\nCancelled"}, {"name": "Patient Encounter-custom_annotations", "dt": "Patient Encounter", "fieldname": "custom_annotations", "label": "Annotations", "fieldtype": "Table", "creation": "2024-08-11 14:28:06.653918", "reqd": 0, "insert_after": "procedure_prescription", "description": None, "options": "Health Annotation Table"}, {"name": "Patient Encounter-custom_encounter_state", "dt": "Patient Encounter", "fieldname": "custom_encounter_state", "label": "Encounter State", "fieldtype": "Select", "creation": "2024-08-08 12:42:51.163180", "reqd": 0, "insert_after": "custom_appointment_category", "description": None, "options": "Consultation\nProcedure\nFollow-up\nSession"}, {"name": "Patient Encounter-custom_illness_progression", "dt": "Patient Encounter", "fieldname": "custom_illness_progression", "label": "Illness Progression", "fieldtype": "Small Text", "creation": "2024-08-06 10:24:28.546753", "reqd": 0, "insert_after": "custom_illness_progression_section", "description": None, "options": None}, {"name": "Patient Encounter-custom_other_examination", "dt": "Patient Encounter", "fieldname": "custom_other_examination", "label": "Other Examination", "fieldtype": "Small Text", "creation": "2024-08-06 10:23:44.635450", "reqd": 0, "insert_after": "custom_physical_examination", "description": None, "options": None}, {"name": "Patient Encounter-custom_physical_examination", "dt": "Patient Encounter", "fieldname": "custom_physical_examination", "label": "Physical Examination", "fieldtype": "Small Text", "creation": "2024-08-06 10:23:44.515775", "reqd": 0, "insert_after": "lab_test_prescription", "description": None, "options": None}, {"name": "Patient Encounter-custom_illness_progression_section", "dt": "Patient Encounter", "fieldname": "custom_illness_progression_section", "label": "Illness Progression", "fieldtype": "Section Break", "creation": "2024-08-06 10:18:24.013385", "reqd": 0, "insert_after": "diagnosis_in_print", "description": None, "options": None}, {"name": "Patient Encounter-custom_section_break_w6rwb", "dt": "Patient Encounter", "fieldname": "custom_section_break_w6rwb", "label": "", "fieldtype": "Section Break", "creation": "2024-08-06 10:12:59.513153", "reqd": 0, "insert_after": "diagnosis_in_print", "description": None, "options": None}, {"name": "Patient Encounter-custom_diagnosis_note", "dt": "Patient Encounter", "fieldname": "custom_diagnosis_note", "label": "Diagnosis Note", "fieldtype": "Small Text", "creation": "2024-08-06 10:12:59.400053", "reqd": 0, "insert_after": "custom_differential_diagnosis", "description": None, "options": None}, {"name": "Patient Encounter-custom_differential_diagnosis", "dt": "Patient Encounter", "fieldname": "custom_differential_diagnosis", "label": "Differential Diagnosis", "fieldtype": "Table MultiSelect", "creation": "2024-08-06 10:12:59.298659", "reqd": 0, "insert_after": "diagnosis", "description": None, "options": "Patient Encounter Diagnosis"}, {"name": "Patient Encounter-custom_symptoms_notes", "dt": "Patient Encounter", "fieldname": "custom_symptoms_notes", "label": "Symptoms Notes", "fieldtype": "Small Text", "creation": "2024-08-06 10:12:59.177981", "reqd": 0, "insert_after": "custom_symptoms_duration", "description": None, "options": None}, {"name": "Patient Encounter-custom_symptoms_duration", "dt": "Patient Encounter", "fieldname": "custom_symptoms_duration", "label": "Symptoms Duration", "fieldtype": "Int", "creation": "2024-08-06 10:12:59.057656", "reqd": 0, "insert_after": "symptoms", "description": None, "options": None}, {"name": "Patient Encounter-custom_encounter_start_time", "dt": "Patient Encounter", "fieldname": "custom_encounter_start_time", "label": "Encounter Start Time", "fieldtype": "Datetime", "creation": "2024-07-14 20:33:58.769868", "reqd": 0, "insert_after": "encounter_time", "description": None, "options": None}, {"name": "Patient Encounter-custom_appointment_category", "dt": "Patient Encounter", "fieldname": "custom_appointment_category", "label": "Appointment Category", "fieldtype": "Data", "creation": "2024-06-20 08:43:59.348003", "reqd": 0, "insert_after": "appointment_type", "description": None, "options": None}, {"name": "Patient Encounter-custom_attachments", "dt": "Patient Encounter", "fieldname": "custom_attachments", "label": "Attachments", "fieldtype": "Table", "creation": "2024-05-30 09:43:47.208759", "reqd": 0, "insert_after": "section_break_33", "description": None, "options": "Patient Encounter Attachments"}, {"name": "Service Request-auto_repeat", "dt": "Service Request", "fieldname": "auto_repeat", "label": "Auto Repeat", "fieldtype": "Link", "creation": "2024-06-23 08:52:40.582083", "reqd": 0, "insert_after": "billing_status", "description": None, "options": "Auto Repeat"}]

