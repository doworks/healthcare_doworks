import frappe
import datetime
import json
from healthcare.healthcare.doctype.patient_appointment.patient_appointment import update_status

# App Resources
@frappe.whitelist()
def fetch_resources():
	user_name = frappe.session.user
	user_image = frappe.db.get_value('User', user_name, 'user_image')
	practitioners = frappe.db.get_list('Healthcare Practitioner', fields=['practitioner_name', 'image', 'department', 'name'])
	patients = frappe.db.get_list('Patient', fields=['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile'])
	appointmentTypes = frappe.db.get_list('Appointment Type', fields=['appointment_type', 'allow_booking_for', 'default_duration'])
	departments = frappe.db.get_list('Medical Department', fields=['department'])
	serviceUnits = frappe.db.get_list('Healthcare Service Unit', fields=['name'], filters={'allow_appointments': 1})
	diagnosis = frappe.db.get_list('Diagnosis', fields=['diagnosis'])
	complaints = frappe.db.get_list('Complaint', fields=['complaints'])
	medications = frappe.db.get_list('Medication', fields=['name'])
	items = frappe.db.get_list('Item', fields=['name', 'item_name'])
	dosageForms = frappe.db.get_list('Dosage Form', fields=['dosage_form'])
	prescriptionDosages = frappe.db.get_list('Prescription Dosage', fields=['dosage'])
	prescriptionPeriods = frappe.db.get_list('Prescription Duration', fields=['name'])
	labTestTemplates = frappe.db.get_list('Lab Test Template', fields=['name', 'department'])
	return {
		'user': {'name': user_name, 'image': user_image},
		'practitioners': practitioners,
		'patients': patients,
		'appointmentTypes': appointmentTypes,
		'departments': departments,
		'serviceUnits': serviceUnits,
		'diagnosis': diagnosis,
		'complaints': complaints,
		'medications': medications,
		'items': items,
		'dosageForms': dosageForms,
		'prescriptionDosages': prescriptionDosages,
		'prescriptionDurations': prescriptionPeriods,
		'labTestTemplates': labTestTemplates
	}

# Appointments Page
@frappe.whitelist()
def fetch_patient_appointments():
	return get_appointments()

@frappe.whitelist()
def reschedule_appointment(form):
	update_status(form['name'], 'Cancelled')

	form['name'] = ''
	new_doc = frappe.get_doc(form)
	new_doc.insert()
	update_status(new_doc.name, 'Rescheduled')
	get_appointments()

@frappe.whitelist()
def transferToPractitioner(app, practitioner):
	doc = frappe.get_doc('Patient Appointment', app)
	doc.practitioner = practitioner
	doc.custom_visit_status = 'Transferred'
	doc.save()

@frappe.whitelist()
def change_status(docname, status):
	doc = frappe.get_doc('Patient Appointment', docname)
	doc.custom_visit_status = status
	doc.append("custom_appointment_time_logs", {
		"status": status,
		"time": datetime.datetime.now()
	})
	doc.save()

# Patient Encounter Page
@frappe.whitelist()
def patient_encounter_records(appointment):
	if(appointment):
		appointment = frappe.get_doc('Patient Appointment', appointment)
		patient = frappe.get_doc('Patient', appointment.patient)
		practitioner = frappe.get_doc('Healthcare Practitioner', appointment.practitioner)
		vital_signs = frappe.db.get_list('Vital Signs',
			filters={'patient': appointment.patient},
			fields=[
				'signs_date', 'signs_time', 'temperature', 'pulse', 'respiratory_rate', 'tongue', 'abdomen', 'name',
				'reflexes', 'bp_systolic', 'bp_diastolic', 'vital_signs_note', 'height', 'weight', 'bmi', 'nutrition_note'
			],
			order_by='signs_date desc, signs_time desc',
		)
		encounters = frappe.db.sql("""
			SELECT
				pe.`name` AS `name`,
				pe.`encounter_date` AS `date`,
				pe.`encounter_time` AS `time`,
				pe.`practitioner_name` AS `practitioner_name`,
				pe.`medical_department` AS `medical_department`,
				pe.`patient_name` AS `patient_name`,
				pa.`custom_appointment_category` AS `appointment_category`,

				JSON_ARRAYAGG(s.complaint) AS `symptoms`,
				JSON_ARRAYAGG(d.diagnosis) AS `diagnosis`
				
			FROM
				`tabPatient Encounter` pe
			LEFT JOIN `tabPatient Appointment` pa
				ON pa.`name` = pe.`appointment`
			LEFT JOIN `tabPatient Encounter Symptom` s
				ON s.`parent` = pe.`name`
			LEFT JOIN `tabPatient Encounter Diagnosis` d
				ON s.`parent` = pe.`name`
			WHERE
				pe.`patient_name` = %(patient)s
			GROUP BY
				pe.`name`
			ORDER BY
				pe.`encounter_date` DESC,
				pe.`encounter_time` DESC
		""", values={'patient': appointment.patient}, as_dict=True)
		for encounter in encounters:
			encounter['symptoms'] = json.loads(encounter['symptoms'])
			encounter['diagnosis'] = json.loads(encounter['diagnosis'])
		return {'appointment': appointment, 'vitalSigns': vital_signs, 'encounters': encounters, 'patient': patient, 'practitioner': practitioner}


@frappe.whitelist()
def new_doc(form, submit=False):
	doc = frappe.get_doc(form)
	doc.insert()
	if(submit):
		doc.submit()

def get_appointments(*args):
	appointments = frappe.db.sql("""
		SELECT
			pa.`name` AS `appointment_id`,
			pa.`patient_name` AS `patient_name`,
			pa.`status` AS `status`,
			pa.`custom_visit_status` AS `visit_status`,
			pa.`custom_appointment_category` AS `appointment_category`,
			pa.`appointment_type` AS `appointment_type`,
			pa.`appointment_for` AS `appointment_for`,
			pa.`practitioner_name` AS `practitioner_name`,
			pa.`practitioner` AS `practitioner`,
			hp.image AS `practitioner_image`,
			pa.`department` AS `department`,
			pa.`service_unit` AS `service_unit`,
			pa.`duration` AS `duration`,
			pa.`notes` AS `notes`,
			pa.`appointment_date` AS `appointment_date`,
			pa.`appointment_time` AS `appointment_time`,
			pa.`custom_appointment_category` AS `appointment_category`,
			pa.`service_unit` AS `service_unit`,
			pa.`custom_payment_type` AS `payment_type`,

			JSON_OBJECT(
				'id', `tabPatient`.`name`,
				'image', `tabPatient`.`image`,
				'mobile', `tabPatient`.`mobile`,
				'gender', `tabPatient`.`sex`,
				'age', pa.`patient_age`,
				'cpr', `tabPatient`.`custom_cpr`,
				'date_of_birth', `tabPatient`.`dob`
			) AS `patient_details`,
							  
			JSON_ARRAYAGG(
				JSON_OBJECT(
					'provider', vn.`provider`,
					'note', vn.`note`,
					'time', vn.`time`
				)
			) AS `visit_notes`,
							  
			JSON_ARRAYAGG(
				JSON_OBJECT(
					'status', tl.`status`,
					'time', tl.`time`
				)
			) AS `status_log`
			
		FROM
			`tabPatient Appointment` pa
		LEFT JOIN `tabPatient`
			ON `tabPatient`.`name` = pa.`patient`
		LEFT JOIN `tabHealthcare Practitioner` hp
			ON hp.`name` = pa.`practitioner`
		LEFT JOIN `tabAppointment Note Table` vn
			ON vn.`parent` = pa.`name`
		LEFT JOIN `tabAppointment Time Logs` tl
			ON tl.`parent` = pa.`name`
		WHERE
			pa.`status` IN ('Scheduled', 'Rescheduled', 'Walked In')
		GROUP BY
    		pa.`name`
		ORDER BY
			pa.`appointment_date` ASC,
    		pa.`appointment_time` ASC
	""", as_dict=True)
	frappe.publish_realtime("patient_appointments", appointments)
	return appointments