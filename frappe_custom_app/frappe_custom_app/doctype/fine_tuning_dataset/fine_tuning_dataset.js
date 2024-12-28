// Copyright (c) 2024, duongtk and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Fine Tuning Dataset", {
// 	refresh(frm) {

// 	},
// });

frappe.listview_settings['Fine Tuning Dataset'] = {
    onload: function (listview) {
        // Thêm nút Export trên màn hình danh sách
        listview.page.add_menu_item(__('Export Fine-Tuning Data'), function () {
            frappe.call({
                method: "frappe_custom_app.frappe_custom_app.doctype.fine_tuning_dataset.fine_tuning_dataset.export_fine_tuning_data",
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint({
                            title: __('Export Successful'),
                            message: __('File saved at: ') + response.message,
                            indicator: 'green'
                        });
                    } else {
                        frappe.msgprint({
                            title: __('Export Failed'),
                            message: __('Unable to export data.'),
                            indicator: 'red'
                        });
                    }
                }
            });
        });
    }
};
