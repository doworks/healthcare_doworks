import frappe
from healthcare.healthcare.doctype.patient_encounter.patient_encounter import PatientEncounter
from healthcare.healthcare.doctype.patient_encounter.patient_encounter import set_codification_table_from_diagnosis

class CustomPatientEncounter(PatientEncounter):
	def validate(self):
		self.set_title()
		self.validate_medications()
		self.validate_therapies()
		self.validate_observations()
		set_codification_table_from_diagnosis(self)
		if not self.is_new() and self.submit_orders_on_save:
			self.make_service_request()
			self.make_medication_request()
			# self.status = "Ordered"