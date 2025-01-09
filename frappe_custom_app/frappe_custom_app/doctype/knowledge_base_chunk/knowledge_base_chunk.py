# Copyright (c) 2025, duongtk and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import json


class KnowledgeBaseChunk(Document):
	def on_update(self):
		if self.status == "Reviewed":
			self.check_all_chunks_reviewed()

	def check_all_chunks_reviewed(self):
		print("check_all_chunks_reviewed")
		# Get total chunks for this Knowledge Base
		total_chunks = frappe.db.count('Knowledge Base Chunk', {'knowledge_base': self.knowledge_base})
		
		# Get reviewed chunks
		reviewed_chunks = frappe.db.count('Knowledge Base Chunk', {
			'knowledge_base': self.knowledge_base,
			'status': 'Reviewed'
		})
		print("total_chunks: ", total_chunks)
		print("reviewed_chunks: ", reviewed_chunks)
		if total_chunks == reviewed_chunks:
			# All chunks reviewed; process them
			knowledge_base_doc = frappe.get_doc('Knowledge Base', self.knowledge_base)
			knowledge_base_doc.process_reviewed_chunks()

@frappe.whitelist()
def bulk_update_status(docnames):
	if not frappe.has_permission('Knowledge Base Chunk', 'write'):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	docnames = frappe.parse_json(docnames)
	knowledge_bases = set()

	# Update chunk statuses and collect knowledge bases
	for name in docnames:
		chunk = frappe.get_doc('Knowledge Base Chunk', name)
		chunk.status = 'Reviewed'
		chunk.save()
		knowledge_bases.add(chunk.knowledge_base)

	frappe.db.commit()

	# Check and process each affected knowledge base
	for kb_name in knowledge_bases:
		check_and_process_knowledge_base(kb_name)

def check_and_process_knowledge_base(kb_name):
	# Fetch total chunks for the knowledge base
	total_chunks = frappe.get_all(
		'Knowledge Base Chunk',
		filters={'knowledge_base': kb_name},
		fields=['name']
	)

	# Fetch reviewed chunks
	reviewed_chunks = frappe.get_all(
		'Knowledge Base Chunk',
		filters={
			'knowledge_base': kb_name,
			'status': 'Reviewed'
		},
		fields=['name']
	)

	if len(total_chunks) == len(reviewed_chunks):
		# All chunks are reviewed; process them
		knowledge_base_doc = frappe.get_doc('Knowledge Base', kb_name)
		if knowledge_base_doc.status != "Completed":
			knowledge_base_doc.process_reviewed_chunks()
