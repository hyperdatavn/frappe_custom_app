// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt

frappe.ui.form.on('Zalo ZNS Settings', {
    refresh: function(frm) {
        frm.add_custom_button(__('Authorize Zalo'), function() {
            frappe.call({
                method: 'frappe_custom_app.frappe_custom_app.doctype.zalo_zns_settings.zalo_zns_settings.generate_code_challenge',
                callback: function(response) {
                    let authorization_url = response.message;
                    window.open(authorization_url, '_blank');
                }
            });
        });

    }
});
