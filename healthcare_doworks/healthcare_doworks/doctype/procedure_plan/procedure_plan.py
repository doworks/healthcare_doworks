# Copyright (c) 2024, S.Mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProcedurePlan(Document):
	@frappe.whitelist()
	def set_procedures_from_template(self):
		if self.plan_template:
			self.procedures = []
			doc = frappe.get_doc('Procedure Plan Template', self.plan_template)
			print(doc.as_dict())
			for procedure in doc.procedures:
				self.append('procedures', {'template': procedure.template})
