frappe.listview_settings['Knowledge Base Chunk'] = {
    onload: function(listview) {
        // Add Bulk Update button
        listview.page.add_action_item(__('Bulk Update to Reviewed'), function() {
            let selected_docs = listview.get_checked_items();
            if (selected_docs.length === 0) {
                frappe.msgprint(__('Please select at least one document to update.'));
                return;
            }

            frappe.confirm(
                __('Are you sure you want to mark {0} selected documents as Reviewed?', [selected_docs.length]),
                function() {
                    // On 'Yes' click
                    frappe.call({
                        method: 'frappe_custom_app.frappe_custom_app.doctype.knowledge_base_chunk.knowledge_base_chunk.bulk_update_status',
                        args: {
                            docnames: selected_docs.map(doc => doc.name)
                        },
                        freeze: true,
                        freeze_message: __('Updating documents...'),
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.show_alert({
                                    message: __('Successfully updated {0} documents', [selected_docs.length]),
                                    indicator: 'green'
                                });
                                listview.refresh();
                            } else {
                                frappe.msgprint(__('An error occurred while updating documents.'));
                            }
                        }
                    });
                }
            );
        });
    }
};

