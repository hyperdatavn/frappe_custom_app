# Copyright (c) 2024, duongtk and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe

class CustomAppSettings(Document):
    def validate(self):
        if "System Manager" not in frappe.get_roles():
            frappe.throw(_("You do not have access to this app"), frappe.PermissionError)
    # pass

# Move the function outside of the class
def get_custom_settings():
    return frappe.get_single("Custom App Settings")
