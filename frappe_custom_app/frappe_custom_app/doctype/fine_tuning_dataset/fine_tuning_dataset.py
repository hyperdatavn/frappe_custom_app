# Copyright (c) 2024, duongtk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class FineTuningDataset(Document):
	pass


@frappe.whitelist()
def export_fine_tuning_data():
    datasets = frappe.get_all("Fine Tuning Dataset", fields=["prompt", "completion"])
    output_file = frappe.get_site_path("private", "files", "fine_tuning_export.jsonl")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for dataset in datasets:
            json.dump({"prompt": dataset["prompt"], "completion": dataset["completion"]}, f, ensure_ascii=False)
            f.write("\n")
    
    return f"Data exported successfully to {output_file}"
