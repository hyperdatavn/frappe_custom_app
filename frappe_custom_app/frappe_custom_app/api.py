import frappe
from frappe import _

@frappe.whitelist(allow_guest=True, methods=["GET"])
def login_via_wiki_user(email: str):
    """
    Custom API to login as a wiki user and redirect to the wiki page.
    """
    # Check if "allow_default_wiki_user" is enabled in "Hyperdata App Settings"
    allow_default_wiki_user = frappe.db.get_single_value("Hyperdata App Settings", "allow_default_wiki_user")
    if not allow_default_wiki_user:
        # Exit if allow_default_wiki_user is False
        frappe.respond_as_web_page(
            _("Not Permitted"),
            _("The login feature is not enabled."),
            http_status_code=403,
            indicator_color="red",
        )
        return

    # Check if the user is already logged in
    if frappe.session.user != "Guest":
        # Redirect to the wiki home page with the current user profile
        redirect_to_wiki()
    else:
        # If email is authorized and the user is not logged in, log in as the wiki user
        if email == "wiki@gmail.com":
            # Log the user in as the wiki user
            frappe.local.login_manager.login_as(email)
            
            # Redirect to the wiki home page
            redirect_to_wiki()
        else:
            # If email is not allowed, return a 403 forbidden response
            frappe.respond_as_web_page(
                _("Not Permitted"),
                _("The link you're trying to use is invalid or expired."),
                http_status_code=403,
                indicator_color="red",
            )

def redirect_to_wiki():
    """
    Redirect the logged-in user to the /wiki/home page.
    """
    frappe.local.response["type"] = "redirect"
    redirect_to = frappe.utils.get_url("/wiki/home")
    frappe.local.response["location"] = redirect_to
