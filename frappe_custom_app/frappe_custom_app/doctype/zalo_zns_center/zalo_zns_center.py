# Copyright (c) 2024, duongtk and contributors
# For license information, please see license.txt

import json
import os
import frappe
import requests
from frappe import get_site_config
from frappe.model.document import Document

class ZaloZNSCenter(Document):
	pass

def get_new_access_token():
    # Fetch Zalo ZNS settings
    settings = frappe.get_single("Zalo ZNS Settings")
    app_id = settings.app_id
    app_secret = settings.app_secret
    refresh_token = settings.refresh_token

    if not (app_id and app_secret and refresh_token):
        frappe.throw("Zalo ZNS settings are not properly configured.")

    url = 'https://oauth.zaloapp.com/v4/access_token'
    payload = {
        'app_id': app_id,
        'app_secret': app_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()

        if 'access_token' in data:
            # Optionally, update settings with the new access token if needed
            return data['access_token']
        else:
            frappe.throw(f"Failed to refresh access token: {data.get('error_description', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to refresh access token: {e}")
        
def get_access_token():
    # Load site config
    settings = frappe.get_single("Zalo ZNS Settings")
    access_token = settings.access_token
    if not access_token:
        access_token = get_new_access_token()
        
    # Need to add a logic to check access token is expired ? 
    # Call get_new_access_token 
    
    return access_token

@frappe.whitelist()
def fetch_zalo_templates():
    # settings = frappe.get_single("Zalo ZNS Setting")
    access_token = get_access_token()  # Ensure this function is implemented to get a new token

    url = 'https://business.openapi.zalo.me/template/all?offset=0&limit=100'
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            templates = data['data']
            return [{"value": tpl["templateId"], "label": tpl["templateName"]} for tpl in templates]
        else:
            frappe.throw(f"Failed to fetch templates: {data.get('error_description', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to fetch templates: {e}")


@frappe.whitelist()
def get_example_template_data(template_id):
    access_token = get_access_token()  # Ensure this function is implemented to get a new token

    url = f'https://business.openapi.zalo.me/template/sample-data?template_id={template_id}'
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            example_data = data['data']
            return json.dumps(example_data, indent=4)
        else:
            frappe.throw(f"Failed to fetch example data: {data.get('error_description', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to fetch example data: {e}")
        
        
@frappe.whitelist()
def send_zalo_notification(phone_number, template_id, template_data, tracking_id, mode="development"):
    access_token = get_access_token()
    url = 'https://business.openapi.zalo.me/message/template'
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }
    
    # Ensure template_data is treated as an object (dictionary)
    try:
        template_data_dict = frappe.parse_json(template_data)
    except ValueError:
        frappe.throw("Invalid template_data format. Expected JSON object.")
    
    payload = {
        "mode": mode,
        "phone": phone_number,
        "template_id": template_id,
        "template_data": template_data_dict,
        "tracking_id": tracking_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 401:  # Unauthorized - possibly due to invalid/expired token
            print("Access token expired or invalid, refreshing token...")
            access_token = get_new_access_token()
            headers['access_token'] = access_token
            response = requests.post(url, headers=headers, json=payload)
            
        response_data = response.json()    
        # Check for specific error in response text
        if response_data.get('error') == -111:
            err_msg = response_data.get('message')
            frappe.throw(f"Failed to send notification: {err_msg}")
                

        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to send notification: {e}")
        