import frappe
from healthcare.healthcare.doctype.patient_encounter.patient_encounter import PatientEncounter
from healthcare.healthcare.doctype.patient_encounter.patient_encounter import set_codification_table_from_diagnosis

class CustomPatientEncounter(PatientEncounter):
	def validate(self):
		self.set_title()
		# self.validate_medications()
		self.validate_therapies()
		self.validate_observations()
		set_codification_table_from_diagnosis(self)
		if not self.is_new() and self.submit_orders_on_save:
			self.make_service_request()
			self.make_medication_request()
			# self.status = "Ordered"

	def on_update(self):
		# if self.appointment:
		# 	frappe.db.set_value("Patient Appointment", self.appointment, "status", "Closed")
		pass

	def on_cancel(self):
		self.db_set("status", "Cancelled")

		if self.appointment:
			# frappe.db.set_value("Patient Appointment", self.appointment, "status", "Open")
			frappe.db.set_value("Patient Appointment", self.appointment, "custom_visit_status", "Cancelled")

		if self.inpatient_record and self.drug_prescription:
			delete_ip_medication_order(self)