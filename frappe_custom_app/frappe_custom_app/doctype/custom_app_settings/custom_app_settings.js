// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt
frappe.ui.form.on('Custom App Settings', {
    refresh: function (frm) {
        frm.add_custom_button(__('View Document'), function () {
            // Open the API URL in a new tab
            const host = "https://apps.hyperdata.vn"
            const email = "wiki@gmail.com"
            const apiUrl = `${host}/api/method/frappe_custom_app.frappe_custom_app.api.login_via_wiki_user?email=${email}`;
            window.open(apiUrl, '_blank');
        });
    }
});
