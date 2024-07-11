# Copyright (c) 2024, duongtk and contributors
# For license information, please see license.txt

import json
import os
import frappe
import requests
from frappe.model.document import Document
from frappe import _, msgprint
from frappe.utils import cstr


class ZaloZNSCenter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.
 
	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		branch: DF.Link | None
		customer: DF.Link | None
		department: DF.Link | None
		message: DF.Text
		receiver_list: DF.Code | None
		sales_partner: DF.Link | None
		send_to: DF.Literal[
			"",
			"All Contact",
			"All Customer Contact",
			"All Supplier Contact",
			"All Sales Partner Contact",
			"All Lead (Open)",
			"All Employee (Active)",
			"All Sales Person",
		]
		supplier: DF.Link | None
		total_characters: DF.Int
		total_messages: DF.Int
	# end: auto-generated types

	@frappe.whitelist()
	def create_receiver_list(self):
		rec, where_clause = "", ""
		if self.send_to == "All Customer Contact":
			where_clause = " and dl.link_doctype = 'Customer'"
			if self.customer:
				where_clause += (
					" and dl.link_name = '%s'" % self.customer.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to == "All Supplier Contact":
			where_clause = " and dl.link_doctype = 'Supplier'"
			if self.supplier:
				where_clause += (
					" and dl.link_name = '%s'" % self.supplier.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to == "All Sales Partner Contact":
			where_clause = " and dl.link_doctype = 'Sales Partner'"
			if self.sales_partner:
				where_clause += (
					"and dl.link_name = '%s'" % self.sales_partner.replace("'", "'")
					or " and ifnull(dl.link_name, '') != ''"
				)
		if self.send_to in [
			"All Contact",
			"All Customer Contact",
			"All Supplier Contact",
			"All Sales Partner Contact",
		]:
			rec = frappe.db.sql(
				"""select CONCAT(ifnull(c.first_name,''), ' ', ifnull(c.last_name,'')),
				c.mobile_no from `tabContact` c, `tabDynamic Link` dl  where ifnull(c.mobile_no,'')!='' and
				c.docstatus != 2 and dl.parent = c.name%s"""
				% where_clause
			)

		elif self.send_to == "All Lead (Open)":
			rec = frappe.db.sql(
				"""select lead_name, mobile_no from `tabLead` where
				ifnull(mobile_no,'')!='' and docstatus != 2 and status='Open'"""
			)

		elif self.send_to == "All Employee (Active)":
			where_clause = (
				self.department and " and department = '%s'" % self.department.replace("'", "'") or ""
			)
			where_clause += self.branch and " and branch = '%s'" % self.branch.replace("'", "'") or ""

			rec = frappe.db.sql(
				"""select employee_name, cell_number from
				`tabEmployee` where status = 'Active' and docstatus < 2 and
				ifnull(cell_number,'')!='' %s"""
				% where_clause
			)

		elif self.send_to == "All Sales Person":
			rec = frappe.db.sql(
				"""select sales_person_name,
				tabEmployee.cell_number from `tabSales Person` left join tabEmployee
				on `tabSales Person`.employee = tabEmployee.name
				where ifnull(tabEmployee.cell_number,'')!=''"""
			)

		rec_list = ""
		for d in rec:
			rec_list += d[0] + " - " + d[1] + "\n"
		self.receiver_list = rec_list

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
    access_token = get_access_token()

    url = 'https://business.openapi.zalo.me/template/all?offset=0&limit=100'
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:  # Unauthorized - possibly due to invalid/expired token
            print("Access token expired or invalid, refreshing token...")
            access_token = get_new_access_token()
            headers['access_token'] = access_token
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
        if response.status_code == 401:  # Unauthorized - possibly due to invalid/expired token
            print("Access token expired or invalid, refreshing token...")
            access_token = get_new_access_token()
            headers['access_token'] = access_token
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
def send_zalo_notification(receiver_list, template_id, template_data, tracking_id, mode="development"):
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

    receiver_nos = []
    if receiver_list:
        for d in receiver_list.split("\n"):
            receiver_no = d
            if "-" in d:
                receiver_no = receiver_no.split("-")[1]
            receiver_no = receiver_no.strip()
            if receiver_no.startswith("0"):
                receiver_no = "+84" + receiver_no[1:]
            if receiver_no:
                receiver_nos.append(cstr(receiver_no).strip())
    else:
        msgprint(_("Receiver List is empty. Please create Receiver List"))
    
    try:
        for phone in receiver_nos: 
            payload = {
                # "mode": mode, // Turn on this mode in localhost for testing
                "phone": phone,
                "template_id": template_id,
                "template_data": template_data_dict,
                "tracking_id": tracking_id
            }
            response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 401:  # Unauthorized - possibly due to invalid/expired token
            print("Access token expired or invalid, refreshing token...")
            access_token = get_new_access_token()
            headers['access_token'] = access_token
            response = requests.post(url, headers=headers, json=payload)
            
        response_data = response.json()    
        # print("response_data: ", response_data)
        # Check for specific error in response text
        if response_data.get('error') == -111:
            err_msg = response_data.get('message')
            frappe.throw(f"Failed to send notification: {err_msg}")
                

        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to send notification: {e}")
        