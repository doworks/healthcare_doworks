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

	def set_status():
		pass

	@frappe.whitelist()
	def change_status(self, status):
		self.custom_visit_status = status
		self.append("custom_appointment_time_logs", {
			"status": status,
			"time": frappe.utils.get_datetime()
		})
		self.save()

	def on_update(self):
		prev_doc = self.get_doc_before_save() or frappe._dict()
		current = self.get("custom_visit_status")
		prev = prev_doc.get("custom_visit_status")
		if current != prev and (current == "Arrived" or prev == "Arrived"):
			waiting_list = frappe.db.sql("""
                SELECT pa.name, pa.patient_name, pa.patient, pa.practitioner, at.time as arrival_time, pa.appointment_time, pa.appointment_date
                FROM `tabPatient Appointment` pa
                LEFT JOIN `tabAppointment Time Logs` at ON pa.name = at.parent AND at.status = 'Arrived'
                WHERE pa.custom_visit_status = 'Arrived' AND pa.appointment_date = CURDATE()
                ORDER BY at.time DESC
			""", as_dict=True)
   
			frappe.publish_realtime("waiting_list", waiting_list)
