import frappe
import faiss
import numpy as np
import json
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from frappe.model.document import Document
import os

MAX_DISTANCE = 2.0  # Define maximum distance for FAISS similarity normalization

class KnowledgeBaseQuery(Document):
    pass

@frappe.whitelist()
def process_query(docname):
    """
    Process the user's query: Vector search → GPT → Response.
    """
    print("docname: ", docname)
    # Ensure the document exists before proceeding
    if not frappe.db.exists("Knowledge Base Query", docname):
        frappe.throw(f"Document {docname} not found.")
    # Fetch the document
    knowledge_query = frappe.get_doc("Knowledge Base Query", docname)

    # Ensure the OpenAI API key is configured
    fields = frappe.db.get_value("Hyperdata App Settings", None, ['api_key', 'model'])
    api_key, model = fields if fields else (None, "gpt-3.5-turbo")
    if not api_key:
        frappe.throw("OpenAI API key is missing. Please configure it in Hyperdata App Settings.")

    # Initialize embeddings and GPT
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    llm = OpenAI(api_key=api_key, model=model)

    # Ensure FAISS index and metadata paths
    faiss_index_path = frappe.get_site_path("private", "files", "faiss_index.bin")
    metadata_path = frappe.get_site_path("private", "files", "faiss_metadata.json")

    try:
        # Update status to "Processing"
        knowledge_query.status = "Processing"
        knowledge_query.save()
        frappe.db.commit()

        # Get user query and embed it
        user_query = knowledge_query.user_query
        user_vector = embeddings.embed_query(user_query)
        print("Query Vector Length:", len(user_vector))
        print("First 5 Elements of Vector:", user_vector[:5])

        # Load FAISS index and metadata
        if not os.path.exists(faiss_index_path) or not os.path.exists(metadata_path):
            frappe.throw("No knowledge base vectors found. Please index some documents first.")

        index = faiss.read_index(faiss_index_path)
        if index.ntotal == 0:
            frappe.throw("Knowledge base index is empty. Please index some documents first.")
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        # Query FAISS for relevant texts
        top_k = 3
        distances, indices = index.search(np.array([user_vector], dtype="float32"), top_k)
        print("Distances:", distances)
        print("Indices:", indices)
        # Ensure valid indices and extract texts
        relevant_texts = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0:
                metadata_entry = metadata[idx]
                relevant_text = {
                    'text': metadata_entry.get('description', ''),
                    'section': metadata_entry.get('section_title', ''),
                    'source': metadata_entry.get('file_name', ''),
                    'relevance': 1.0 - (distance / MAX_DISTANCE)
                }
                relevant_texts.append(relevant_text)

        # Sort by relevance
        relevant_texts.sort(key=lambda x: x['relevance'], reverse=True)

        # If no relevant texts are found, set a default message
        if not relevant_texts:
            relevant_texts.append("No relevant texts found for the query.")

        # Join the relevant texts into a single string to use in GPT prompt
        context = "\n".join([text['text'] for text in relevant_texts])
        print("context: ", context)
        # Generate GPT prompt
        gpt_prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="You are an assistant with legal knowledge. Based on the following context:\n{context}\n\nAnswer the user's question by vietnamese:\n{query}"
        ).format(context=context, query=user_query)

        # Store the full prompt before asking GPT
        knowledge_query.full_prompt = gpt_prompt
        
        # Ask GPT
        gpt_response = llm(gpt_prompt)

        # Update the Knowledge Base Query document with results
        knowledge_query.relevant_texts = context
        knowledge_query.response = gpt_response
        knowledge_query.status = "Completed"
        knowledge_query.save()
        frappe.db.commit()

        # Return success message
        return {"message": "success", "response": gpt_response}

    except Exception as e:
        # Handle errors
        knowledge_query.status = "Failed"
        knowledge_query.response = f"Error: {str(e)}"
        knowledge_query.save()
        frappe.db.commit()
        frappe.log_error(frappe.get_traceback(), "Knowledge Base Query Error")
        raise e
