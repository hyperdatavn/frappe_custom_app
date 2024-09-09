
import frappe
from urllib.parse import quote
from frappe import _

def show_custom_signup():
    # Check if custom signup form is enabled
    if frappe.db.get_single_value("Custom App Settings", "use_custom_signup_form"):
        return "frappe_custom_app/templates/signup-form.html"
    
    # Check if LMS Settings DocType exists
    if frappe.db.exists("DocType", "LMS Settings"):
        # Check if terms of use or privacy policy is set
        if frappe.db.get_single_value("LMS Settings", "terms_of_use") or frappe.db.get_single_value("LMS Settings", "privacy_policy"):
            return "lms/templates/signup-form.html"
    
    return "frappe/templates/signup.html"
