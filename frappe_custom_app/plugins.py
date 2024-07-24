
import frappe
from urllib.parse import quote
from frappe import _

def show_custom_signup():
	return "frappe_custom_app/templates/signup-form.html"
	# if frappe.db.get_single_value(
	# 	"LMS Settings", "terms_of_use"
	# ) or frappe.db.get_single_value("LMS Settings", "privacy_policy"):
	# 	return "lms/templates/signup-form.html"
	# return "frappe/templates/signup.html"
