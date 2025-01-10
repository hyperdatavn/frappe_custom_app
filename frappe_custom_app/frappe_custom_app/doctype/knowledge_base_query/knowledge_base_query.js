// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt


frappe.ui.form.on("Knowledge Base Query", {
    submit_asking: function (frm) {
        // Check if the user query is empty
        if (!frm.doc.user_query) {
            frappe.msgprint(__("Please enter a query before submitting."));
            return;
        }

        // First save the document
        frm.save().then(() => {
            // After successful save, call the server-side function
            frappe.call({
                method: "frappe_custom_app.frappe_custom_app.doctype.knowledge_base_query.knowledge_base_query.process_query",
                args: {
                    docname: frm.docname
                },
                freeze: true,
                freeze_message: __("Processing your query..."),
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint(__("Query processed successfully!"));
                        frm.reload_doc(); // Reload to show updated values
                    }
                },
                error: function (err) {
                    console.error("Error while processing query:", err);
                    frappe.msgprint(__("An error occurred while processing the query."));
                }
            });
        }).catch((err) => {
            console.error("Error saving document:", err);
            frappe.msgprint(__("Please save the document first."));
        });
    },
    
    refresh: function(frm) {
        frm.refresh_fields(['full_prompt', 'response', 'relevant_texts']);
    }
});
