import frappe
from frappe import _

app_name = "healthcare_doworks"
app_title = "Healthcare Doworks"
app_publisher = "S.Mohamed"
app_description = "An extention for the healthcare frappe app"
app_email = "sayed10998@gmail.com"
app_license = "mit"

# required_apps = []
add_to_apps_screen = [
	{
		"name": "frontend",
		"logo": "/assets/healthcare/images/healthcare.png",
		"title": "Healthcare",
		"route": "/frontend",
        "has_permission": "healthcare_doworks.api.methods.check_app_permission",
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/healthcare_doworks/css/jquery-ui.min.css",
    "/assets/healthcare_doworks/css/bootstrap-popover-x.min.css",
    "/assets/frappe/node_modules/air-datepicker/dist/css/datepicker.min.css"
]
app_include_js = [
	"/assets/healthcare_doworks/js/calendar.js",
	"/assets/healthcare_doworks/js/lib/imagemapster/jquery.imagemapster.min.js",
	"/assets/healthcare_doworks/js/lib/p5/p5.min.js",
	"/assets/healthcare_doworks/js/humanize-duration.js",
	"/assets/healthcare_doworks/js/jquery-ui.min.js",
	"/assets/healthcare_doworks/js/bootstrap-popover-x.min.js",
	"/assets/healthcare_doworks/js/humanize-duration.js",
	"/assets/healthcare_doworks/js/customscript.js",
	"/assets/frappe/node_modules/air-datepicker/dist/js/datepicker.min.js",
	"/assets/frappe/node_modules/air-datepicker/dist/js/i18n/datepicker.en.js"
	# "/assets/do_health/js/lib/fullcalendar/fullcalendar.min.js"
	# "/assets/do_health/js/patient_appointment.js"
]
# include js, css files in header of web template
# web_include_css = "/assets/healthcare_doworks/css/healthcare_doworks.css"
# web_include_js = "/assets/healthcare_doworks/js/healthcare_doworks.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "healthcare_doworks/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
page_js = {"appointment-calendar" : "/assets/frappe/node_modules/air-datepicker/dist/js/datepicker.min.js"}
page_js = {"appointment-calendar" : "/assets/frappe/node_modules/air-datepicker/dist/js/i18n/datepicker.en.js"}
page_js = {"appointment-calendar" : "/assets/frappe/js/frappe/views/calendar/calendar.js"}

# include js in doctype views
doctype_js = {
	# "Patient" : "public/js/patient.js",
	"Patient Appointment" : "public/js/patient_appointment.js",
	# "Patient Encounter" : "public/js/patient_encounter.js",
 	# "Clinical Procedure" : "public/js/clinical_procedure.js"
}
doctype_list_js = {
	"Patient Appointment" : "public/js/patient_appointment_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
	"Patient Appointment" : [
		"public/js/patient_appointment_calendar.js",
		"/assets/healthcare_doworks/js/humanize-duration.js"
	]
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "healthcare_doworks/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#       "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#       "methods": "healthcare_doworks.utils.jinja_methods",
#       "filters": "healthcare_doworks.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "healthcare_doworks.install.before_install"
# after_install = "healthcare_doworks.install.after_install"
after_install = "healthcare_doworks.install.add_custom_fields"

# Uninstallation
# ------------

# before_uninstall = "healthcare_doworks.uninstall.before_uninstall"
# after_uninstall = "healthcare_doworks.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "healthcare_doworks.utils.before_app_install"
# after_app_install = "healthcare_doworks.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "healthcare_doworks.utils.before_app_uninstall"
# after_app_uninstall = "healthcare_doworks.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "healthcare_doworks.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#       "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#       "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Patient Appointment": "healthcare_doworks.overrides.patient_appointment.CustomPatientAppointment",
    "Test Patient Appointment": "healthcare_doworks.overrides.test_patient_appointment.CustomTestPatientAppointment",
    "Patient Encounter": "healthcare_doworks.overrides.patient_encounter.CustomPatientEncounter"
}

# app_include_js = "healthcare_doworks.overrides.healthcare_service_unit.js"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
#       "*": {
#               "on_update": "method",
#               "on_cancel": "method",
#               "on_trash": "method"
#       }
    'Patient':{
        "on_update": "healthcare_doworks.api.events.patient_update"
    },
    'Patient Appointment':{
        "after_insert": "healthcare_doworks.api.events.patient_appointment_inserted",
        "on_update": "healthcare_doworks.api.methods.get_appointments"
    },
    'Patient Encounter':{
        "after_insert": "healthcare_doworks.api.events.patient_encounter_inserted",
        "on_update": "healthcare_doworks.api.events.patient_encounter_update",
        "on_submit": "healthcare_doworks.api.events.patient_encounter_submit"
    },
    'Clinical Procedure':{
        "on_update": "healthcare_doworks.api.events.clinical_procedure_update",
    },
    'Service Request':{
        "on_update": "healthcare_doworks.api.methods.get_services"
    },
    'Medication Request':{
        "on_update": "healthcare_doworks.api.events.medication_request_update",
        "on_submit": "healthcare_doworks.api.events.medication_request_update"
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "all": [
        "healthcare_doworks.api.methods.mark_no_show_appointments"
    ],
}

# scheduler_events = {
#       "all": [
#               "healthcare_doworks.tasks.all"
#       ],
#       "daily": [
#               "healthcare_doworks.tasks.daily"
#       ],
#       "hourly": [
#               "healthcare_doworks.tasks.hourly"
#       ],
#       "weekly": [
#               "healthcare_doworks.tasks.weekly"
#       ],
#       "monthly": [
#               "healthcare_doworks.tasks.monthly"
#       ],
# }

# Testing
# -------

# before_tests = "healthcare_doworks.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#       "frappe.desk.doctype.event.event.get_events": "healthcare_doworks.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#       "Task": "healthcare_doworks.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["healthcare_doworks.utils.before_request"]
# after_request = ["healthcare_doworks.utils.after_request"]

# Job Events
# ----------
# before_job = ["healthcare_doworks.utils.before_job"]
# after_job = ["healthcare_doworks.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#       {
#               "doctype": "{doctype_1}",
#               "filter_by": "{filter_by}",
#               "redact_fields": ["{field_1}", "{field_2}"],
#               "partial": 1,
#       },
#       {
#               "doctype": "{doctype_2}",
#               "filter_by": "{filter_by}",
#               "partial": 1,
#       },
#       {
#               "doctype": "{doctype_3}",
#               "strict": False,
#       },
#       {
#               "doctype": "{doctype_4}"
#       }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#       "healthcare_doworks.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
#       "Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Custom Field", "filters": {"module": "Healthcare Doworks"}},
	{"dt": "Property Setter", "filters": {"module": "Healthcare Doworks"}},
]

on_logout = "healthcare_doworks.api.methods.on_logout"

website_route_rules = [{'from_route': '/frontend/<path:app_path>', 'to_route': 'frontend'},]

socketio_debug = True