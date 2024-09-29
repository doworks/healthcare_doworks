import frappe
from frappe import _
import datetime
import frappe.query_builder
import frappe.query_builder.functions
from frappe.utils import add_to_date, get_datetime, get_datetime_str
from frappe.utils.file_manager import save_file
# from healthcare.healthcare.doctype.patient_appointment.patient_appointment import update_status
from frappe.utils.pdf import get_pdf
import os
import base64
import re

# App Resources
@frappe.whitelist()
def fetch_resources():
	user = frappe.get_doc('User', frappe.session.user)
	user_practitioner = frappe.db.get_value('Healthcare Practitioner', {'user_id': user.name}, ['name', 'practitioner_name', 'image', 'department'])
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
		'siteName': frappe.local.site
	}

# Appointments Page
@frappe.whitelist()
def get_tabs_count(filters):
	total_count = {'Scheduled': 0, 'Arrived': 0, 'Ready': 0, 'In Room': 0, 'Completed': 0, 'No Show': 0}
	for key, value in total_count.items():
		count_filter = dict(filters)
		count_filter['custom_visit_status'] = key
		total_count[key] = frappe.db.count('Patient Appointment', count_filter)

	return total_count

@frappe.whitelist()
def fetch_patient_appointments(filters=None, start=0, limit=50):
	dic = {}
	total_count = {'Scheduled': 0, 'Arrived': 0, 'Ready': 0, 'In Room': 0, 'Completed': 0, 'No Show': 0}
	for key, value in total_count.items():
		count_filter = dict(filters)
		count_filter['custom_visit_status'] = key
		total_count[key] = frappe.db.count('Patient Appointment', count_filter)
	dic['total_count'] = total_count

	appointments = frappe.get_list(
		'Patient Appointment',
		filters=filters,
		fields=[
			'name', 'patient_name', 'status', 'custom_visit_status', 'custom_appointment_category',
			'appointment_type', 'appointment_for', 'practitioner_name', 'practitioner',
			'department', 'service_unit', 'duration', 'notes', 'appointment_date', 'appointment_time',
			'custom_payment_type', 'patient_age', 'patient', 'custom_confirmed', 'custom_customer'
		],
		order_by='appointment_date asc, appointment_time asc',
		start=start,
		page_length=limit
	)
	for appointment in appointments:
		appointment = get_appointment_details(appointment)
	dic['appointments'] = appointments

	return dic

@frappe.whitelist()
def fetch_nurse_records():
	return {
		'appointments': get_appointments(),
		'services': get_services(),
	}

@frappe.whitelist()
def reschedule_appointment(form):
	appointment = frappe.get_doc('Patient Appointment', form['name'])
	appointment.custom_visit_status = 'Cancelled'
	appointment.status = 'Cancelled'
	appointment.save()

	form['name'] = ''
	new_doc = frappe.get_doc(form)
	new_doc.status = 'Rescheduled'
	new_doc.insert()

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

@frappe.whitelist()
def fetch_nurse_records():
	users = frappe.db.get_all('User', filters={'status': 'Active'}, fields=['name', 'full_name'],)
	return users

# Patient Encounter Page
@frappe.whitelist()
def patient_encounter_name(appointment_id):
	if(frappe.db.exists('Patient Appointment', appointment_id)):
		appointment = frappe.get_doc('Patient Appointment', appointment_id)
		if frappe.db.exists('Patient Encounter', {"appointment": appointment_id}):
			return frappe.db.get_list('Patient Encounter', filters={"appointment": appointment_id}, pluck='name')[-1]
		else:
			patient = frappe.get_doc('Patient', appointment.patient)
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
			if patient.dob:
				new_encounter.patient_age = calculate_age(patient.dob)
			loggedin_practitioner = frappe.db.get_value('Healthcare Practitioner', {'user_id': frappe.session.user}, ['name', 'practitioner_name'])
			if loggedin_practitioner is not None:
				new_encounter.practitioner = loggedin_practitioner[0]
				new_encounter.practitioner_name = loggedin_practitioner[1]
			else:
				new_encounter.practitioner = appointment.practitioner
				new_encounter.practitioner_name = appointment.practitioner_name
			new_encounter.insert()
		
			# assign default values for the procedure
			if appointment.custom_appointment_category == 'Procedure':
				procedure = frappe.new_doc('Clinical Procedure')
				procedure.procedure_template = appointment.custom_procedure_template
				procedure.custom_patient_encounter = new_encounter.name
				procedure.patient = new_encounter.patient
				procedure.patient_name = new_encounter.patient_name
				procedure.patient_sex = new_encounter.patient_sex
				procedure.patient_age = new_encounter.patient_age
				procedure.practitioner = new_encounter.practitioner
				procedure.practitioner_name = new_encounter.practitioner_name
				procedure.medical_department = new_encounter.medical_department
				procedure.service_unit = appointment.service_unit
				procedure.insert()
			return new_encounter.name
@frappe.whitelist()
def patient_encounter_records(encounter_id):
	if(frappe.db.exists('Patient Encounter', encounter_id)):
		current_encounter = frappe.get_doc('Patient Encounter', encounter_id)
		appointment = frappe.get_doc('Patient Appointment', current_encounter.appointment)
		patient = frappe.get_doc('Patient', appointment.patient)
		practitioner = frappe.get_doc('Healthcare Practitioner', appointment.practitioner)
		procedures = []
		if frappe.db.exists('Clinical Procedure', {"custom_patient_encounter": current_encounter.name}):
			procedures_list = frappe.db.get_list('Clinical Procedure', filters={"custom_patient_encounter": current_encounter.name}, pluck='name')
			for procedure in procedures_list:
				procedures.append(frappe.get_doc('Clinical Procedure', procedure))

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
		encounters = frappe.db.get_list('Patient Encounter', filters={"status": ['!=', 'Cancelled'], 'patient': patient.name}, pluck='name')
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
			'procedures': procedures
		}

@frappe.whitelist()
def submit_encounter(encounter):
	doc = frappe.get_doc('Patient Encounter', encounter)
	doc.submit()
	procedures = frappe.get_list('Clinical Procedure', filters={'custom_patient_encounter': encounter})
	for procedure in procedures:
		procedure_doc = frappe.get_doc('Clinical Procedure', procedure)
		procedure_doc.submit()
	return doc

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
def upload_annotation(docname, doctype, annotation_template, encounter_type='', file_data=None, jsonText='', annotation_type='Free Drawing'):
	if not file_data:
		frappe.throw("File data is missing")

	health_annotation = frappe.new_doc('Health Annotation')
	health_annotation.annotation_type = annotation_type
	health_annotation.annotation_template = annotation_template
	health_annotation.json = jsonText
	health_annotation.insert()
	# Parse the data URL to get the file type and the Base64 data
	if file_data.startswith('data:image'):
		header, base64_data = file_data.split(',', 1)
		# Extract the file extension from the header
		extension = header.split('/')[1].split(';')[0]
		file_name = f"annotation.{extension}"
	else:
		frappe.throw("Invalid file data")

	# Decode the Base64 string
	file_content = base64.b64decode(base64_data)

	# Save the file
	file_doc = save_file(file_name, file_content, health_annotation.doctype, health_annotation.name, is_private=1)

	# Update the doctype with the file URL
	health_annotation.image = file_doc.file_url
	health_annotation.save()
	
	doc = frappe.get_doc(doctype, docname)
	doc.append("custom_annotations", {
		"annotation": health_annotation.name,
		"type": encounter_type,
	})
	doc.save()

	return {"file_url": file_doc.file_url}

@frappe.whitelist()
def annotations_records():
	templates = frappe.db.get_list('Annotation Template', fields= ['label', 'gender', 'kid', 'image', 'name'], order_by='creation asc',)
	treatments = frappe.db.get_list('Annotation Treatment', fields= ['treatment', 'name', 'color'])
	for treatment in treatments:
		treatment.variables = frappe.db.get_all('Treatment Variables Table', fields=['variable_name', 'type', 'options'], filters={'parent': treatment.name})
	return {'templates': templates, 'treatments': treatments}

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
def save_patient_history(patient='', 
	allergies=None , 
	infected_diseases=None, 
	surgical_history=None, 
	medicaitons=None, 
	habits=None, 
	risk_factors=None,
	chronic_diseases='',
	genetic_diseases=''):
	doc = frappe.get_doc('Patient', patient)
	if allergies:
		doc.custom_allergies_table = []
		for item in allergies:
			del item['name']
			doc.append("custom_allergies_table", item)
	if infected_diseases:
		doc.custom_infected_diseases = []
		for item in infected_diseases:
			if 'creation' in item:
				del item['name']
			doc.append("custom_infected_diseases", item)
	if surgical_history:
		doc.custom_surgical_history_table = []
		for item in surgical_history:
			if 'creation' in item:
				del item['name']
			doc.append("custom_surgical_history_table", item)
	if medicaitons:
		doc.custom_medications = []
		for item in medicaitons:
			if 'creation' in item:
				del item['name']
			doc.append("custom_medications", item)
	if habits:
		doc.custom_habits__social = []
		for item in habits:
			if 'creation' in item:
				del item['name']
			doc.append("custom_habits__social", item)
	if risk_factors:
		doc.custom_risk_factors_table = []
		for item in risk_factors:
			if 'creation' in item:
				del item['name']
			doc.append("custom_risk_factors_table", item)
	doc.custom_chronic_diseases = chronic_diseases
	doc.custom_genetic_conditions = genetic_diseases
	doc.custom_medical_history_last_updated = frappe.utils.now()
	doc.save()

@frappe.whitelist()
def patient(patient=''):
	doc = frappe.get_doc('Patient', patient)
	return {'doc': doc}

@frappe.whitelist()
def pos_payment_method(pos_profile):
	return frappe.get_all('POS Payment Method',
        fields=['default', 'mode_of_payment'],
        filters={'parent': pos_profile}
	)

@frappe.whitelist()
def create_invoice(appointment, profile, payment_methods):
	appointment_doc = frappe.get_doc('Patient Appointment', appointment)
	patient = frappe.get_doc('Patient', appointment_doc.patient)
	branches = frappe.db.get_all('Branch', order_by='creation', pluck='name')
	branch = branches[0] if branches else ''
	customer_invoice_row = False
	insurance_invoice_row = False
	for invoice_item in appointment_doc.custom_invoice_items:
		if not invoice_item.customer_invoice:
			customer_invoice_row = True
		if not invoice_item.insurance_invoice:
			insurance_invoice_row = True

	if appointment_doc.custom_payment_type == 'Self Payment' and customer_invoice_row:
		invoice = frappe.new_doc('Sales Invoice')
		invoice.patient = patient.name
		invoice.patient_name = patient.patient_name
		invoice.is_pos = 1
		invoice.pos_profile = profile
		invoice.customer = patient.customer
		invoice.posting_date = frappe.utils.now()
		invoice.due_date = frappe.utils.now()
		invoice.service_unit = appointment_doc.service_unit
		invoice.branch = appointment_doc.custom_branch or branch or ''
		for invoice_item in appointment_doc.custom_invoice_items:
			if not invoice_item.customer_invoice:
				invoice.append('items', {
					'item_code': invoice_item.item,
					'item_name': invoice_item.item_name,
					'uom': invoice_item.item_uom,
					'qty': invoice_item.quantity,
					'rate': invoice_item.rate,
					'amount': invoice_item.amount,
				})
		for method in payment_methods:
			invoice.append('payments', {
				'default': method.get('default', 0),
				'mode_of_payment': method.get('mode_of_payment', ''),
				'amount': method.get('amount', 0),
				'reference_no': method.get('reference_no', '')
			})
		invoice.save()
		invoice.submit()
		for invoice_item in appointment_doc.custom_invoice_items:
			if not invoice_item.customer_invoice:
				invoice_item.customer_invoice = invoice.name
		appointment_doc.save()
		return {'customer_invoice': invoice.name}
	elif appointment_doc.custom_payment_type == 'Insurance' and (customer_invoice_row or insurance_invoice_row):
		if customer_invoice_row:
			patient_invoice = frappe.new_doc('Sales Invoice')
			patient_invoice.patient = patient.name
			patient_invoice.patient_name = patient.patient_name
			patient_invoice.is_pos = 1
			patient_invoice.pos_profile = profile
			patient_invoice.customer = patient.customer
			patient_invoice.posting_date = frappe.utils.now()
			patient_invoice.due_date = frappe.utils.now()
			patient_invoice.service_unit = appointment_doc.service_unit
			patient_invoice.branch = appointment_doc.custom_branch or branch or ''
			for invoice_item in appointment_doc.custom_invoice_items:
				if not invoice_item.customer_invoice:
					patient_invoice.append('items', {
						'item_code': invoice_item.item,
						'item_name': invoice_item.item_name,
						'uom': invoice_item.item_uom,
						'qty': invoice_item.quantity,
						'rate': float(invoice_item.customer_amount) / float(invoice_item.quantity),
						'amount': invoice_item.customer_amount,
					})
			for method in payment_methods:
				patient_invoice.append('payments', {
					'default': method.default,
					'mode_of_payment': method.mode_of_payment,
					'amount': method.amount,
					'reference_no': method.reference_no
				})
			patient_invoice.save()
			patient_invoice.submit()

		if insurance_invoice_row:
			insurance_invoice = frappe.new_doc('Sales Invoice')
			insurance_invoice.patient = patient.name
			insurance_invoice.patient_name = patient.patient_name
			insurance_invoice.is_pos = 0
			insurance_invoice.customer = patient.custom_insurance_company_name
			insurance_invoice.posting_date = frappe.utils.now()
			insurance_invoice.due_date = frappe.utils.now()
			insurance_invoice.service_unit = appointment_doc.service_unit
			insurance_invoice.branch = appointment_doc.custom_branch or branch or ''
			for invoice_item in appointment_doc.custom_invoice_items:
				if not invoice_item.insurance_invoice:
					insurance_invoice.append('items', {
						'item_code': invoice_item.item,
						'item_name': invoice_item.item_name,
						'uom': invoice_item.item_uom,
						'qty': invoice_item.quantity,
						'rate': float(invoice_item.insurance_amount) / float(invoice_item.quantity),
						'amount': invoice_item.insurance_amount,
					})
			insurance_invoice.save()
			insurance_invoice.submit()

		for invoice_item in appointment_doc.custom_invoice_items:
			if not invoice_item.customer_invoice:
				invoice_item.customer_invoice = patient_invoice.name
				
			if not invoice_item.insurance_invoice:
				invoice_item.insurance_invoice = insurance_invoice.name
				
		appointment_doc.save()
		return {'insurance_invoice': insurance_invoice.name, 'customer_invoice': patient_invoice.name}

@frappe.whitelist()
def make_payment(appointment, mode_of_payment, reference_no=None, reference_date=None):
	appointment_doc = frappe.get_doc('Patient Appointment', appointment)
	invoices = list(d["customer_invoice"] for d in appointment_doc.as_dict()['custom_invoice_items'] if d["customer_invoice"])
	mop = frappe.get_doc('Mode of Payment', mode_of_payment)
	
	for invoice in invoices:
		invoice_doc = frappe.get_doc('Sales Invoice', invoice)
		if invoice_doc.status != 'Paid':
			payment_entry = frappe.new_doc('Payment Entry')
			payment_entry.mode_of_payment = mode_of_payment
			payment_entry.party_type = 'Customer'
			payment_entry.party = invoice_doc.customer
			payment_entry.party_name = invoice_doc.customer_name
			payment_entry.paid_amount = invoice_doc.grand_total

			payment_entry.paid_to = mop.accounts[0].default_account
			payment_entry.received_amount = invoice_doc.grand_total
			payment_entry.source_exchange_rate = 1
			payment_entry.target_exchange_rate = 1

			payment_entry.append('references', {
				'reference_doctype': 'Sales Invoice',
				'reference_name': invoice,
				'due_date': invoice_doc.due_date,
				'total_amount': invoice_doc.grand_total,
				'outstanding_amount': invoice_doc.outstanding_amount,
				'allocated_amount': invoice_doc.outstanding_amount
			})
			if reference_no:
				payment_entry.reference_no = reference_no
			if reference_date:
				payment_entry.reference_date = reference_date

			payment_entry.save()
			payment_entry.submit()
		

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
def new_doc(form, children={}, submit=False):
	doc = frappe.get_doc(form)
	if children:
		for key, items in children.items():
			for item in items:
				doc.append(key, item)
	doc.insert()
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

def get_services(doc=None, method=None):
	services = frappe.db.get_list('Service Request',
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
	frappe.publish_realtime("services", services)
	return services

def get_appointments(doc=None, method=None):
	if doc:  # Check if the appointment document exists
		appointment = get_appointment_details(doc.as_dict())
		frappe.publish_realtime(
			event="patient_appointments_updated",
			message=appointment,
			after_commit=True
		)

def get_appointment_details(appointment):
	# Get patient details
	patient_details = frappe.get_doc('Patient', appointment['patient'])
	appointment['patient_details'] = {
		'id': patient_details.name,
		'image': patient_details.image,
		'mobile': patient_details.mobile,
		'gender': patient_details.sex,
		'age': appointment['patient_age'],
		'cpr': patient_details.custom_cpr,
		'date_of_birth': patient_details.dob
	}

	# Get latest vital signs for the patient
	vital_signs = frappe.get_list('Vital Signs', 
		filters={
			'patient': appointment['patient']
		},
		fields=['height', 'weight', 'bmi', 'nutrition_note'],
		order_by='signs_date desc',
		limit=1
	)
	if vital_signs:
		appointment.update(vital_signs[0])

	# Get the last visit date
	last_visit = frappe.get_list('Patient Encounter', 
		filters={
			'patient': appointment['patient']
		},
		fields=['encounter_date'],
		order_by='encounter_date desc',
		limit=1
	)
	if last_visit:
		appointment['last_visit'] = last_visit[0]['encounter_date']

	# Get visit notes
	to_options = ['', frappe.session.user, frappe.session.full_name]
	visit_notes = frappe.get_all('Appointment Note Table',
		filters={'parent': appointment['name'], 'to': ['in', to_options]},
		fields=['to', 'full_name', 'note', 'time', 'read', 'from']
	)
	appointment['visit_notes'] = visit_notes

	# Get status log
	status_log = frappe.get_all('Appointment Time Logs',
		filters={'parent': appointment['name']},
		fields=['status', 'time']
	)
	appointment['status_log'] = status_log

	# Get invoice items
	invoice_items = frappe.get_all('Healthcare Invoice Item', 
		filters={'parent': appointment['name']},
		fields=['*']
	)
	appointment['invoice_items'] = invoice_items

	# Get practitioner image
	practitioner = frappe.get_doc('Healthcare Practitioner', appointment['practitioner'])
	appointment['practitioner_image'] = practitioner.image if practitioner else None
	return appointment

def calculate_age(dob):
	today = datetime.datetime.today()
	age_years = today.year - dob.year
	age_months = today.month - dob.month
	age_days = today.day - dob.day

	# Adjust for cases where the current day/month is less than the birth day/month
	if age_days < 0:
		age_months -= 1
		last_month = today.month - 1 if today.month > 1 else 12
		last_month_year = today.year if today.month > 1 else today.year - 1
		days_in_last_month = (datetime.datetime(last_month_year, last_month + 1, 1) - datetime.datetime(last_month_year, last_month, 1)).days
		age_days += days_in_last_month

	if age_months < 0:
		age_years -= 1
		age_months += 12

	return f"{age_years} Year(s) {age_months} Month(s) {age_days} Day(s)"

def check_app_permission():
	# if frappe.session.user == "Administrator":
	# 	return True

	# roles = frappe.get_roles()
	# if any(role in ["System Manager", "Sales User", "Sales Manager", "Sales Master Manager"] for role in roles):
	# 	return True

	return True

def mark_no_show_appointments():
    # mark appointmens as no-show if the appointment time has passed 15 minutes
	appointments = frappe.db.sql("""
		SELECT name FROM `tabPatient Appointment`
		WHERE custom_visit_status = 'Scheduled'
		AND CAST((CONCAT(CAST(appointment_date as DATE), ' ', CAST(appointment_time as TIME))) as DATETIME) >= CAST(%(datetime_str)s as DATETIME)
	""", {'datetime_str': get_datetime_str(add_to_date(get_datetime(), minutes=-15))}, as_dict=True)

	# Loop through appointments and mark as no-show
	for appointment in appointments:
		change_status(appointment.name, 'No Show')

def on_logout(): 
	frappe.publish_realtime("session_logout")