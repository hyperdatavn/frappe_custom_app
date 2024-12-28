// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt

frappe.ui.form.on('Web Crawler', {
    refresh: function(frm) {
        frm.add_custom_button(__('Start Crawling'), function() {
            frm.call({
                doc: frm.doc,
                method: 'start_crawling',
                freeze: true,
                freeze_message: __('Crawling website...'),
                callback: function(r) {
                    frm.reload_doc();
                }
            });
        });
    }
});
