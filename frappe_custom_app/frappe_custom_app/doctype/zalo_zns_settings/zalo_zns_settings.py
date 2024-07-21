# Copyright (c) 2024, duongtk and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import base64
import hashlib
import requests
import os
import frappe


class ZaloZNSSettings(Document):
	pass

@frappe.whitelist()
def generate_code_challenge():
    settings = frappe.get_doc("Zalo ZNS Settings")
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode('utf-8')
    
    settings.code_verifier = code_verifier
    settings.code_challenge = code_challenge
    
    state = frappe.generate_hash(length=32)
    settings.state = state
    
    # Generate the redirect URL
    # base_url = frappe.utils.get_url()
    request = frappe.local.request
    hostname = request.host

    redirect_uri = f"https://{hostname}/api/method/frappe_custom_app.frappe_custom_app.doctype.zalo_zns_settings.zalo_zns_settings.handle_zalo_callback"
    settings.redirect_uri = redirect_uri
    
    settings.save()
    frappe.db.commit()

    authorization_url = f"https://oauth.zaloapp.com/v4/permission?app_id={settings.app_id}&redirect_uri={redirect_uri}&code_challenge={code_challenge}&state={state}"
    return authorization_url

@frappe.whitelist()
def get_access_token(authorization_code):
    settings = frappe.get_doc("Zalo ZNS Settings")
    token_url = "https://oauth.zaloapp.com/v4/access_token"
    payload = {
        "app_id": settings.app_id,
        "app_secret": settings.app_secret,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "code_verifier": settings.code_verifier,
    }
    
    response = requests.post(token_url, data=payload)
    token_data = response.json()
    
    settings.access_token = token_data.get('access_token')
    settings.refresh_token = token_data.get('refresh_token')
    settings.save()
    frappe.db.commit()
    return token_data

@frappe.whitelist(allow_guest=True)
def handle_zalo_callback():
    authorization_code = frappe.form_dict.get('code')
    state = frappe.form_dict.get('state')
    code_challenge = frappe.form_dict.get('code_challenge')

    settings = frappe.get_doc("Zalo ZNS Settings")
    if state != settings.state:
        frappe.throw("State does not match")
        
    if code_challenge != settings.code_challenge:
        frappe.throw("Code challenge does not match")    

    get_access_token(authorization_code)

    frappe.msgprint("OAuth flow completed successfully.")
    # Return an HTML page with a success message and a close button
    return """
    <html>
    <head>
        <title>OAuth Flow Completed</title>
    </head>
    <body>
        <h1>OAuth flow completed successfully.</h1>
        <button onclick="window.close()">Close</button>
    </body>
    </html>
    """
