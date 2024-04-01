import frappe

@frappe.whitelist()
def fetch_appointments():
	return frappe.db.sql("""
		SELECT
			pa.`name` AS `appointment_id`,
			pa.`patient` AS `patient_id`,
			pa.`appointment_date` AS `appointment_date`,
			pa.`appointment_time` AS `appointment_time`,
			`tabComment`.`content` AS `comment_text`
		FROM
			`tabPatient Appointment` pa
		LEFT JOIN `tabComment`
			ON `tabComment`.`reference_name` = pa.`name`
		ORDER BY
			pa.`appointment_date` DESC,
			pa.`appointment_time` DESC
	""")