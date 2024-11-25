// Copyright (c) 2024, S.Mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Procedure Plan", {
	refresh(frm) {

	},

    plan_template: function(frm) {
		if (frm.doc.plan_template) {
            frm.call('set_procedures_from_template')
            .then(r => {
                if (r.message) {
                    refresh_field('procedures');
                }
            })
		}
	},
});
