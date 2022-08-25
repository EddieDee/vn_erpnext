from . import __version__ as app_version

app_name = "berenice"
app_title = "Berenice"
app_publisher = "Verynice SRL"
app_description = "Berenice app"
app_icon = "fa fa-paper-plane"
app_color = "red"
app_email = "info@verynice.do"
app_license = "verynice"

fixtures = [{"doctype":"Custom Field", "filters":[
	["name","in",
	("Sales Invoice-ncf",
	"Sales Invoice-mncf",
	"Sales Invoice-customer_type",
	"Sales Invoice-tax_id_type", 
	"Sales Invoice-generate_ncf",
	"POS Invoice-ncf",
	"POS Invoice-mncf",
	"POS Invoice-customer_type",
	"POS Invoice-tax_id_type", 
	"POS Invoice-generate_ncf"
	)]
]}, "Client Script"]

doc_events = {
    "Sales Invoice": {
            "before_submit":'berenice.berenice.csales_invoice.ncf_autoname',
            "autoname":'berenice.berenice.csales_invoice.invoice_autoname',
        },
    "POS Invoice": {
            "before_submit":'berenice.berenice.cpos_invoice.ncf_autoname',
            "autoname":'berenice.berenice.cpos_invoice.invoice_autoname',
        },
    "Purchase Invoice": {
            "before_submit":'berenice.berenice.cpurchase_invoice.mncf_autoname'
        }
 }

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/berenice/css/berenice.css"
# app_include_js = "/assets/berenice/js/berenice.js"

# include js, css files in header of web template
# web_include_css = "/assets/berenice/css/berenice.css"
# web_include_js = "/assets/berenice/js/berenice.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "berenice/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "berenice.install.before_install"
# after_install = "berenice.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "berenice.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"berenice.tasks.all"
# 	],
# 	"daily": [
# 		"berenice.tasks.daily"
# 	],
# 	"hourly": [
# 		"berenice.tasks.hourly"
# 	],
# 	"weekly": [
# 		"berenice.tasks.weekly"
# 	]
# 	"monthly": [
# 		"berenice.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "berenice.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "berenice.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "berenice.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"berenice.auth.validate"
# ]

