// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt

// Declare a global variable to store the template list
var zaloTemplates = [];

frappe.ui.form.on('Zalo ZNS Center', {
    refresh: function(frm) {
        frm.add_custom_button(__('Send ZNS'), function() {
            frm.trigger('send_zns');
        });
        // Only fetch templates if the doc is not new
        frappe.call({
            method: 'frappe_custom_app.frappe_custom_app.doctype.zalo_zns_center.zalo_zns_center.fetch_zalo_templates',
            callback: function(r) {
                if (r.message) {
                    // Store the template list in the global variable
                    zaloTemplates = r.message;
                    frm.set_df_property('template_id', 'options', r.message);
                }
            }
        });

    },
    template_id: function(frm) {
        // Provide example template data when template_id is selected
        let template_id = frm.doc.template_id;
        if (template_id) {
            // Fetch and display an example template data structure
            frappe.call({
                method: 'frappe_custom_app.frappe_custom_app.doctype.zalo_zns_center.zalo_zns_center.get_example_template_data',
                args: { template_id: template_id },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('template_data', r.message);
                    }
                }
            });

            // Use the global variable to set the template name
            let template = zaloTemplates.find(tpl => tpl.value == template_id);
            if (template) {
                frm.set_value('template_name', template.label);
            }
        }
    },
    send_zns: function(frm) {
        // Validate the phone number
        let phone_number = frm.doc.send_to;
        if (!phone_number.startsWith('84')) {
            frappe.msgprint(__('Phone number must start with 84'));
            return;
        }

        // Call the server method to send zns
        frappe.call({
            method: 'frappe_custom_app.frappe_custom_app.doctype.zalo_zns_center.zalo_zns_center.send_zalo_notification',
            args: {
                phone_number: frm.doc.send_to,
                template_id: frm.doc.template_id,
                template_data: frm.doc.template_data,
                tracking_id: 'Your tracking ID here'  // You can modify this as per your requirements
            },
            callback: function(r) {
                if (r.message) {
                    frappe.msgprint(__('Notification sent successfully'));
                } else {
                    frappe.msgprint(__('Failed to send notification'));
                }
            }
        });
    }
});
