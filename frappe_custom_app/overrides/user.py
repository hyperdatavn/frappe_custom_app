import hashlib
import frappe
import requests
from frappe import _
from frappe.core.doctype.user.user import User
from frappe.utils import cint, escape_html, random_string
from frappe.website.utils import is_signup_disabled

class CustomUser(User):
	def validate(self):
		super().validate()
		self.validate_username_duplicates()

	def validate_username_duplicates(self):
		while not self.username or self.username_exists():
			self.username = append_number_if_name_exists(
				self.doctype, cleanup_page_name(self.full_name), fieldname="username"
			)
		if " " in self.username:
			self.username = self.username.replace(" ", "")

		if len(self.username) < 4:
			self.username = self.email.replace("@", "").replace(".", "")

@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, birth_date, phone):
	if is_signup_disabled():
		frappe.throw(_("Sign Up is disabled"), _("Not Allowed"))

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": escape_html(full_name),
			"birth_date": birth_date,
			"phone": phone,
			"country": "Vietnam",
			"enabled": 1,
			"new_password": random_string(10),
			"user_type": "Website User",
		}
	)
	user.flags.ignore_permissions = True
	user.flags.ignore_password_policy = True
	user.insert()

	# set default signup role as per Portal Settings
	default_role = frappe.db.get_value("Portal Settings", None, "default_role")
	if default_role:
		user.add_roles(default_role)

	user.add_roles("LMS Student")

	if user.flags.email_sent:
		return 1, _("Please check your email for verification")
	else:
		return 2, _("Please ask your administrator to verify your sign-up")
