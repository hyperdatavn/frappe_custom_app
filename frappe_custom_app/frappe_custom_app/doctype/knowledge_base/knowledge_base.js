// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Knowledge Base", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Knowledge Base', {
    refresh: function (frm) {
        frm.add_custom_button('Store As Vector', function () {
            frappe.call({
                method: "frappe_custom_app.frappe_custom_app.doctype.knowledge_base.knowledge_base.store_content_as_vector",
                args: {
                    docname: frm.doc.name
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint(r.message);
                        frm.reload_doc();
                    }
                }
            });
        });
    }
});
