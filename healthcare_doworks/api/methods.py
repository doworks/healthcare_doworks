import frappe
from frappe import _
import datetime
from frappe.utils.file_manager import save_file
from healthcare.healthcare.doctype.patient_appointment.patient_appointment import update_status
from frappe.utils.pdf import get_pdf
import os
import base64
import re

# App Resources
@frappe.whitelist()
def fetch_resources():
	user = frappe.get_doc('User', frappe.session.user)
	user_practitioner = frappe.db.get_value('Healthcare Practitioner', {'user_id': user.name}, ['name', 'practitioner_name', 'image', 'department'])
	practitioners = frappe.db.get_list('Healthcare Practitioner', fields=['practitioner_name', 'image', 'department', 'name', 'user'])
	patients = frappe.db.get_list('Patient', 
		fields=['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 'inpatient_record', 'inpatient_status'])
	appointmentTypes = frappe.db.get_list('Appointment Type', fields=['name', 'appointment_type', 'allow_booking_for', 'default_duration'])
	departments = frappe.db.get_list('Medical Department', fields=['department'])
	serviceUnits = frappe.db.get_list('Healthcare Service Unit', fields=['name'], filters={'allow_appointments': 1})
	serviceUnitTypes = frappe.db.get_list('Healthcare Service Unit Type', fields=['name'])
	diagnosis = frappe.db.get_list('Diagnosis', fields=['diagnosis'])
	for d in diagnosis:
		d.label = d.diagnosis
		d.value = d.diagnosis
	complaints = frappe.db.get_list('Complaint', fields=['complaints'])
	for c in complaints:
		c.label = c.complaints
		c.value = c.complaints
	medications = frappe.db.get_list('Medication', fields=['name'])
	items = frappe.db.get_list('Item', fields=['name', 'item_name'])
	dosageForms = frappe.db.get_list('Dosage Form', fields=['dosage_form'])
	prescriptionDosages = frappe.db.get_list('Prescription Dosage', fields=['dosage'])
	prescriptionPeriods = frappe.db.get_list('Prescription Duration', fields=['name'])
	labTestTemplates = frappe.db.get_list('Lab Test Template', fields=['name', 'department'])
	codeValues = frappe.db.get_list('Code Value', fields=['name', 'display', 'code_system'])
	docTypes = frappe.db.get_list('Code Value', fields=['name'])
	roles = frappe.db.get_list('Role', fields=['name'], filters={'restrict_to_domain': 'Healthcare'})
	patientCareTypes = frappe.db.get_list('Patient Care Type', fields=['name'])
	therapyTypes = frappe.db.get_list('Therapy Type', fields=['name'])
	clinicalProcedureTemplates = frappe.db.get_list('Clinical Procedure Template', fields=['name'])
	observationTemplate = frappe.db.get_list('Observation Template', fields=['name'])
	healthcareActivity = frappe.db.get_list('Healthcare Activity', fields=['name'])
	clinicalProcedureTemplate = frappe.db.get_list('Clinical Procedure Template', fields=['name'])
	sampleCollections = frappe.db.get_list('Sample Collection', fields=['name'])
	return {
		'user': {'name': user.full_name, 
		   'user': user.name, 
		   'image': user.user_image, 
		   'practitioner': user_practitioner[0] if user_practitioner is not None else None, 
		   'practitioner_name': user_practitioner[1] if user_practitioner is not None else None, 
		   'practitioner_image': user_practitioner[2] if user_practitioner is not None else None, 
		   'practitioner_department': user_practitioner[3] if user_practitioner is not None else None, 
		   'roles': user.roles
		},
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
		'labTestTemplates': labTestTemplates,
		'codeValues': codeValues,
		'docTypes': docTypes,
		'roles': roles,
		'patientCareTypes': patientCareTypes,
		'serviceUnitTypes': serviceUnitTypes,
		'therapyTypes': therapyTypes,
		'clinicalProcedureTemplates': clinicalProcedureTemplates,
		'observationTemplate': observationTemplate,
		'healthcareActivity': healthcareActivity,
		'clinicalProcedureTemplate': clinicalProcedureTemplate,
		'sampleCollections': sampleCollections,
	}

# Appointments Page
@frappe.whitelist()
def fetch_patient_appointments():
	return get_appointments()

@frappe.whitelist()
def fetch_nurse_records():
	return {
		'appointments': get_appointments(),
		'services': get_services(),
	}

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
def patient_encounter_records(appointment_id):
	if(frappe.db.exists('Patient Appointment', appointment_id)):
		appointment = frappe.get_doc('Patient Appointment', appointment_id)
		patient = frappe.get_doc('Patient', appointment.patient)
		practitioner = frappe.get_doc('Healthcare Practitioner', appointment.practitioner)
		current_encounter = None
		current_procedure = None
		if frappe.db.exists('Patient Encounter', {"appointment": appointment_id}):
			# current_encounter = frappe.get_last_doc('Patient Encounter', filters={"appointment": appointment_id})
			appointment_encounters = frappe.db.get_list('Patient Encounter', filters={"appointment": appointment_id}, pluck='name')
			current_encounter = frappe.get_doc('Patient Encounter', appointment_encounters[-1])
			if frappe.db.exists('Clinical Procedure', {"custom_patient_encounter": current_encounter.name}):
				procedures = frappe.db.get_list('Clinical Procedure', filters={"custom_patient_encounter": current_encounter.name}, pluck='name')
				current_procedure = frappe.get_doc('Clinical Procedure', procedures[-1])
		else:
			new_encounter = frappe.new_doc('Patient Encounter')
			new_encounter.appointment = appointment_id
			new_encounter.encounter_date = frappe.utils.nowdate()
			new_encounter.encounter_time = frappe.utils.nowtime()
			new_encounter.custom_encounter_start_time = frappe.utils.now()

			new_encounter.medical_department = appointment.department
			new_encounter.appointment_type = appointment.appointment_type
			new_encounter.custom_appointment_category = appointment.custom_appointment_category
			new_encounter.patient = patient.name
			new_encounter.patient_name = patient.patient_name
			new_encounter.patient_sex = patient.sex
			new_encounter.patient_age = patient.age
			loggedin_practitioner = frappe.db.get_value('Healthcare Practitioner', {'user_id': frappe.session.user}, ['name', 'practitioner_name'])
			if loggedin_practitioner is not None:
				new_encounter.practitioner = loggedin_practitioner[0]
				new_encounter.practitioner_name = loggedin_practitioner[1]
			else:
				new_encounter.practitioner = appointment.practitioner
				new_encounter.practitioner_name = appointment.practitioner_name
			new_encounter.insert()
			current_encounter = frappe.get_doc('Patient Encounter', new_encounter.name)
		
		# assign default values for the procedure
		if current_procedure == None:
			current_procedure = {
				'custom_patient_encounter': current_encounter.name,
				'patient': current_encounter.patient,
				'patient_name': current_encounter.patient_name,
				'patient_sex': current_encounter.patient_sex,
				'patient_age': current_encounter.patient_age,
				'practitioner': current_encounter.practitioner,
				'practitioner_name': current_encounter.practitioner_name,
				'medical_department': current_encounter.medical_department,
				'service_unit': appointment.service_unit
			}

		# for d in current_encounter.diagnosis:
		# 	d.label = d.diagnosis
		# 	d.value = d.diagnosis
		# for c in current_encounter.symptoms:
		# 	c.label = c.complaint
		# 	c.value = c.complaint
		vital_signs = frappe.db.get_list('Vital Signs',
			filters={'patient': appointment.patient},
			fields=[
				'signs_date', 'signs_time', 'temperature', 'pulse', 'respiratory_rate', 'tongue', 'abdomen', 'name',
				'reflexes', 'bp_systolic', 'bp_diastolic', 'vital_signs_note', 'height', 'weight', 'bmi', 'nutrition_note'
			],
			order_by='signs_date desc, signs_time desc',
		)
		services = frappe.db.get_list('Service Request',
			filters={'patient': appointment.patient}, 
			fields=[
				'status', 'order_date', 'order_time', 'practitioner', 'practitioner_email', 'medical_department', 'referred_to_practitioner', 
				'source_doc', 'order_group', 'sequence', 'staff_role', 'patient_care_type', 'intent', 'priority', 'quantity', 'dosage_form', 
				'as_needed', 'dosage', 'occurrence_date', 'occurrence_time', 'healthcare_service_unit_type', 'order_description', 
				'patient_instructions', 'template_dt', 'template_dn', 'sample_collection_required', 'qty_invoiced', 'billing_status'
			],
			order_by='order_date desc, order_time desc',
		)
		for service in services:
			practitioner = frappe.get_doc('Healthcare Practitioner', service.practitioner)
			status = frappe.get_doc('Code Value', service.status)
			service.practitioner = practitioner.practitioner_name
			service.status = status.display
		encounters = frappe.db.get_list('Patient Encounter', filters={"status": ['!=', 'Cancelled']}, pluck='name')
		encounter_docs = []
		pdf_extensions = ['pdf']
		word_extensions = ['doc', 'docx', 'dot', 'dotx']
		image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']
		attachments = []
		for encounter in encounters:
			doc = frappe.get_doc('Patient Encounter', encounter)
			for attachment in doc.custom_attachments:
				obj = {}
				obj = attachment.__dict__
				url = obj['attachment']
				if url:
					if url.split('.')[-1] in pdf_extensions:
						obj['type'] = 'pdf'
					elif url.split('.')[-1] in word_extensions:
						obj['type'] = 'word'
					elif url.split('.')[-1] in image_extensions:
						obj['type'] = 'image'
					else:
						obj['type'] = 'unknown'
					attachments.append(obj)
			encounter_docs.append(doc)
			if encounter == current_encounter.name:
				encounters.remove(encounter)
		return {
			'appointment': appointment, 
			'vitalSigns': vital_signs,
			'encounters': encounter_docs, 
			'patient': patient, 
			'practitioner': practitioner, 
			'attachments': attachments,
			'services': services,
			'current_encounter': current_encounter,
			'current_procedure': current_procedure
		}

@frappe.whitelist()
def get_print_html(doctype, docname, print_format=None):
	return frappe.get_print(doctype, docname, print_format=print_format)

@frappe.whitelist()
def upload_signature(docname, doctype, file_data=None):
	if not file_data:
		frappe.throw("File data is missing")

	# Parse the data URL to get the file type and the Base64 data
	if file_data.startswith('data:image'):
		header, base64_data = file_data.split(',', 1)
		# Extract the file extension from the header
		extension = header.split('/')[1].split(';')[0]
		file_name = f"signature.{extension}"
	else:
		frappe.throw("Invalid file data")

	# Decode the Base64 string
	file_content = base64.b64decode(base64_data)

	# Save the file
	file_doc = save_file(
		file_name, file_content, doctype, docname, is_private=1
	)

	# Update the doctype with the file URL
	doc = frappe.get_doc(doctype, docname)
	doc.custom_patient_consent_signature = file_doc.file_url
	doc.save()

	return {"file_url": file_doc.file_url}

@frappe.whitelist()
def vital_signs_list(patient):
	if patient:
		return frappe.db.get_list('Vital Signs', 
			fields=['signs_date', 'signs_time', 'temperature', 'pulse', 'name', 'appointment', 'title', 'modified', 'modified_by', 'patient'],
			filters={'patient': patient}, 
			order_by='signs_date desc, signs_time desc',
		)
	else:
		return frappe.db.get_list('Vital Signs', 
			fields=['signs_date', 'signs_time', 'temperature', 'pulse', 'name', 'appointment', 'title', 'modified', 'modified_by', 'patient'], 
			order_by='signs_date desc, signs_time desc',
		)

@frappe.whitelist()
def edit_doc(form, submit=False):
	doc = frappe.get_doc(form['doctype'], form['name'])
	del form['doctype']
	del form['name']

	for key, value in form.items():
		# Assign the value to the corresponding field in the document
		if (key == 'diagnosis' or key == 'symptoms'):
			for item in value:
				if not item['modified']:
					doc.append(key, item)
					continue
		setattr(doc, key, value)
	doc.save()
	if(submit):
		doc.submit()
	return doc

@frappe.whitelist()
def new_doc(form, submit=False):
	doc = frappe.get_doc(form)
	doc.insert()
	if(doc.doctype == 'Patient Appointment'):
		update_status(doc.name, 'Scheduled')
	if(submit):
		doc.submit()
	return doc

def get_age(delta_st):
	# Regular expression to extract years, months, and days
	pattern = r"years=\+?(\d+), months=\+?(\d+), days=\+?(\d+)"

	# Search for the pattern in the string
	match = re.search(pattern, delta_st)

	if match:
		years = int(match.group(1))
		months = int(match.group(2))
		days = int(match.group(3))

		# Format the output string
		return f"{years} Year(s) {months} Month(s) {days} Day(s)"
	else:
		print("Invalid relativedelta string")

def get_pdf_url(doctype, docname, print_format=None):
	# Get the HTML of the document using the specified print format
	html = frappe.get_print(doctype, docname, print_format=print_format)

	# Generate PDF from the HTML
	pdf_content = get_pdf(html)

	# Define the path to save the PDF
	file_name = f"{docname}.pdf"
	file_path = os.path.join(frappe.get_site_path(), "public", "files", file_name)

	# Write the PDF content to a file
	with open(file_path, "wb") as f:
		f.write(pdf_content)

	# Return the URL to access the PDF
	base_url = frappe.utils.get_url()
	pdf_url = f"{base_url}/files/{file_name}"
	return html

def get_updated_encounter(doc, method):
	frappe.publish_realtime("patient_encounter", doc)
	return doc

def get_services(*args):
	services = frappe.db.get_list('Service Request',
		filters={'staff_role': 'Nursing User'}, 
		fields=[
			'status', 'order_date', 'order_time', 'practitioner', 'practitioner_email', 'medical_department', 'referred_to_practitioner', 
			'source_doc', 'order_group', 'sequence', 'staff_role', 'patient_care_type', 'intent', 'priority', 'quantity', 'dosage_form', 
			'as_needed', 'dosage', 'occurrence_date', 'occurrence_time', 'healthcare_service_unit_type', 'order_description', 'patient',
			'patient_instructions', 'template_dt', 'template_dn', 'sample_collection_required', 'qty_invoiced', 'billing_status'
		],
		order_by='order_date asc, order_time asc',
	)
	for service in services:
		practitioner = frappe.get_doc('Healthcare Practitioner', service.practitioner)
		status = frappe.get_doc('Code Value', service.status)
		service.practitioner = practitioner.practitioner_name
		service.status = status.display
	frappe.publish_realtime("services", service)
	return services

def get_appointments(*args):
	appointments = frappe.db.sql("""
		WITH LatestVitalSigns AS (
			SELECT
				vs.patient,
				vs.height,
				vs.weight,
				vs.bmi,
				vs.nutrition_note
			FROM `tabVital Signs` vs
			INNER JOIN (
				SELECT 
					patient,
					MAX(signs_date) AS latest_signs_date
				FROM `tabVital Signs`
				WHERE height IS NOT NULL AND height != ''
				AND weight IS NOT NULL AND weight != ''
				AND bmi IS NOT NULL AND bmi != ''
				AND nutrition_note IS NOT NULL AND nutrition_note != ''
				GROUP BY patient
			) latest_vs ON vs.patient = latest_vs.patient AND vs.signs_date = latest_vs.latest_signs_date
		),					  
		LastVisit AS (
			SELECT
				pe.`patient`,
				pe.`encounter_date`
			FROM `tabPatient Encounter` pe
			WHERE pe.`encounter_date` = (
				SELECT MAX(pe2.`encounter_date`)
				FROM `tabPatient Encounter` pe2
				WHERE pe2.`patient` = pe.`patient`
			)
		)
							  
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
				'date_of_birth', `tabPatient`.`dob`,
				'height', lvs.`height`,
				'weight', lvs.`weight`,
				'bmi', lvs.`bmi`,
				'last_visit', lpe.`encounter_date`,
				'nutrition_note', lvs.`nutrition_note`
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
		LEFT JOIN LatestVitalSigns lvs
    		ON lvs.`patient` = `tabPatient`.`name`
		LEFT JOIN LastVisit lpe
			ON lpe.`patient` = `tabPatient`.`name`
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