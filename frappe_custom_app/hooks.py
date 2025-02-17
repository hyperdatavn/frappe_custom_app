from . import __version__ as app_version

app_name = "frappe_custom_app"
app_title = "Frappe Custom App"
app_publisher = "duongtk"
app_description = "frappe custom app"
app_email = "hyperdatavn@gmail.com"
app_license = "hyperdatavn"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_custom_app/css/frappe_custom_app.css"
# app_include_js = "/assets/frappe_custom_app/js/frappe_custom_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_custom_app/css/frappe_custom_app.css"
# web_include_js = "/assets/frappe_custom_app/js/frappe_custom_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_custom_app/public/scss/website"

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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "frappe_custom_app.utils.jinja_methods",
#	"filters": "frappe_custom_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_custom_app.install.before_install"
# after_install = "frappe_custom_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_custom_app.uninstall.before_uninstall"
# after_uninstall = "frappe_custom_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "frappe_custom_app.utils.before_app_install"
# after_app_install = "frappe_custom_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "frappe_custom_app.utils.before_app_uninstall"
# after_app_uninstall = "frappe_custom_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_custom_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"User": "frappe_custom_app.overrides.user.CustomUser",
    "Web Template": "frappe_custom_app.overrides.web_template.CustomWebTemplate",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"frappe_custom_app.tasks.all"
#	],
#	"daily": [
#		"frappe_custom_app.tasks.daily"
#	],
#	"hourly": [
#		"frappe_custom_app.tasks.hourly"
#	],
#	"weekly": [
#		"frappe_custom_app.tasks.weekly"
#	],
#	"monthly": [
#		"frappe_custom_app.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "frappe_custom_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "frappe_custom_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "frappe_custom_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappe_custom_app.utils.before_request"]
# after_request = ["frappe_custom_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_custom_app.utils.before_job"]
# after_job = ["frappe_custom_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"frappe_custom_app.auth.validate"
# ]

# frappe_custom_app/hooks.py
override_whitelisted_methods = {
    "frappe_custom_app.frappe_custom_app.doctype.zalo_zns_settings.zalo_zns_settings.handle_zalo_callback": "frappe_custom_app.frappe_custom_app.doctype.zalo_zns_settings.zalo_zns_settings.handle_zalo_callback"
}

signup_form_template = "frappe_custom_app.plugins.show_custom_signup"

# Wiki login api
# hooks.py
# Registering the custom login API
api_methods = {
    "GET /api/method/frappe_custom_app.frappe_custom_app.api.login_via_wiki_user": "frappe_custom_app.frappe_custom_app.api.login_via_wiki_user"
}

# DocType JS
doctype_js = {
    "Knowledge Base Chunk": "public/js/knowledge_base_chunk.js"
}

# DocType List JS
doctype_list_js = {
    "Knowledge Base Chunk": "public/js/knowledge_base_chunk_list.js"
}
