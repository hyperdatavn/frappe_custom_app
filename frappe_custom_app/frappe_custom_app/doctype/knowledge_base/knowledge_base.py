import frappe
import os
import json
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
import faiss
from docx import Document as DocxDocument
from frappe.model.document import Document


class KnowledgeBase(Document):
    """Knowledge Base Document Class"""

    @frappe.whitelist()
    def store_content_as_vector(self):
        """
        Process the uploaded .docx file, extract text, and store it as a vector embedding.
        """
        file_url = self.document_file

        if not file_url:
            frappe.throw("Please upload a document file before preparing data.")

        file_path = frappe.get_site_path("private", file_url.replace("/private/files/", "files/"))
        if os.path.exists(file_path):
            print("File exists at:", file_path)
        else:
            print("File not found!")
               
        # Extract text from the document
        text = self._extract_text_from_document(file_path)
        if not text:
            frappe.throw("Failed to extract text from the document.")

        # Generate vector embeddings
        api_key = frappe.db.get_single_value("Hyperdata App Settings", "api_key")
        if not api_key:
            frappe.throw("OpenAI API key is missing. Please configure it in Hyperdata App Settings.")
        
        document_vector = self._generate_vector_from_text(text, api_key)

        # Store vector in FAISS
        metadata = {
            "file_name":  os.path.basename(file_path),
            "source": self.source,
            "description": text[:100],  # Preview first 100 characters
            "content_length": len(text),
            "update_date": frappe.utils.now()
        }
        self._store_vector_in_faiss(document_vector, metadata)

        # Update document status
        self.processed_data = f"Vector stored with metadata: {metadata}"
        self.status = "Completed"
        self.save()

    def _extract_text_from_document(self, file_path):
        try:
            document = DocxDocument(file_path)
            text = []
            for paragraph in document.paragraphs:
                if paragraph.style.name.startswith("Heading"):  # Ignore heading
                    continue
                if paragraph.text.strip():
                    text.append(paragraph.text.strip())
            return self.filter_text("\n".join(text))
        except Exception as e:
            frappe.throw(f"Error reading the document file: {str(e)}")

    def filter_text(self, text):
        """
        Filter out irrelevant or low-quality text such as headings or boilerplate content.
        """
        filtered_lines = []
        for line in text.split("\n"):
            if len(line.strip()) > 10 and any(c.isalnum() for c in line):
                filtered_lines.append(line.strip())
        return "\n".join(filtered_lines)        

    def _generate_vector_from_text(self, text, api_key):
        """
        Generate a vector embedding for the given text using OpenAI.
        """
        try:
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            return embeddings.embed_query(text)
        except Exception as e:
            frappe.throw(f"Failed to generate embeddings: {str(e)}")

    def _store_vector_in_faiss(self, document_vector, metadata):
        """
        Store vector embeddings and metadata into FAISS index.
        """
        try:
            faiss_index_path = frappe.get_site_path("private", "files", "faiss_index.bin")
            metadata_path = frappe.get_site_path("private", "files", "faiss_metadata.json")

            # Load or initialize FAISS index
            if os.path.exists(faiss_index_path):
                index = faiss.read_index(faiss_index_path)
            else:
                index = faiss.IndexFlatL2(len(document_vector))

            # Load or initialize metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata_list = json.load(f)
            else:
                metadata_list = []

            # Add vector and metadata
            index.add(np.array([document_vector], dtype="float32"))
            metadata_list.append(metadata)

            # Save updated index and metadata
            faiss.write_index(index, faiss_index_path)
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata_list, f, ensure_ascii=False, indent=4)

        except Exception as e:
            frappe.throw(f"Failed to store vector in FAISS: {str(e)}")

@frappe.whitelist()
def store_content_as_vector(docname):
    doc = frappe.get_doc("Knowledge Base", docname)
    return doc.store_content_as_vector()
