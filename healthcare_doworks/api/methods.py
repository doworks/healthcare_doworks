import frappe

@frappe.whitelist()
def fetch_patient_appointments():
	return get_appointments()

@frappe.whitelist()
def reschedule_appointment():
	pass

@frappe.whitelist()
def change_status():
	pass

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
			pa.`custom_visit_note` AS `visit_note`,
			pa.`appointment_date` AS `appointment_date`,
			pa.`appointment_time` AS `appointment_time`,
			pa.`custom_appointment_category` AS `appointment_category`,
			pa.`service_unit` AS `service_unit`,
			

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
		
		ORDER BY
			pa.`appointment_date` DESC,
			pa.`appointment_time` DESC
	""", as_dict=True)
	frappe.publish_realtime("patient_appointments", appointments)
	return appointments