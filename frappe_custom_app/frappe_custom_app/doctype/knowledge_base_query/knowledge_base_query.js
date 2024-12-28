// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt


frappe.ui.form.on("Knowledge Base Query", {
    submit_asking: function (frm) {
        // Check if the user query is empty
        if (!frm.doc.user_query) {
            frappe.msgprint(__("Please enter a query before submitting."));
            return;
        }

        // Save the document first
        frm.save().then(function() {
            // Call the server-side function to process the query
            frappe.call({
                method: "frappe_custom_app.frappe_custom_app.doctype.knowledge_base_query.knowledge_base_query.process_query",
                args: {
                    docname: frm.doc.name // Pass the docname after saving
                },
                freeze: true,
                freeze_message: __("Processing your query..."),
                callback: function (response) {
                    if (response.message) {
                        // Success message
                        frappe.msgprint(__("Query processed successfully!"));
                        frm.reload_doc(); // Reload the form to get updated data
                    } else {
                        // If no response message, handle it gracefully
                        frappe.msgprint(__("Unexpected response. Please try again."));
                    }
                },
                error: function (err) {
                    // Log the error and display a message
                    console.error("Error while processing query:", err);
                    frappe.msgprint(__("An error occurred while processing the query."));
                }
            });
        });
    }
});
