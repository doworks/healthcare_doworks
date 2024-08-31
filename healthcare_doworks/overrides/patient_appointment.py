import frappe
from healthcare.healthcare.doctype.patient_appointment.patient_appointment import PatientAppointment

class CustomPatientAppointment(PatientAppointment):
	def validate(self):
		# self.validate_overlaps()
		self.validate_based_on_appointments_for()
		self.validate_service_unit()
		self.set_appointment_datetime()
		self.validate_customer_created()
		# self.set_status()
		self.set_title()
		self.update_event()
		self.set_postition_in_queue()

	def update_appointment_status():
		# update the status of appointments daily

		# appointments = frappe.get_all(
		# 	"Patient Appointment", {"status": ("not in", ["Closed", "Cancelled"])}
		# )

		# for appointment in appointments:
		# 	appointment_doc = frappe.get_doc("Patient Appointment", appointment.name)
		# 	appointment_doc.set_status()
		# 	appointment_doc.save()
		pass
