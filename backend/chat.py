# backend/chat.py

import logging
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel
import os
from embed import generate_embedding  # ✅ Correct import

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")  # Ensure this is a valid model name
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Configure Gemini
configure(api_key=GEMINI_API_KEY)

# ✅ Establish Weaviate Connection (v4)
try:
    if "weaviate.cloud" in WEAVIATE_URL:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
        )
    else:
        client = weaviate.connect_to_local()

    if not client.is_ready():
        raise Exception("Weaviate connection failed.")
    logging.info("✅ Connected to Weaviate Successfully!")

except Exception as e:
    logging.error(f"❌ Weaviate Connection Failed: {str(e)}")
    client = None

def generate_response(query):
    """Retrieve relevant data from Weaviate and generate a response using Gemini."""
    if not client:
        return "Weaviate connection failed."

    try:
        # ✅ Generate embedding for query
        query_vector = generate_embedding(query)

        # ✅ Correct Weaviate v4 Query Execution
        results = (
            client.collections.get("ScrapedData")
            .query.near_vector(query_vector, limit=3)  # ✅ Correct method for query
        )

        retrieved_data = results.objects

        if not retrieved_data:
            return "No relevant data found."

        context = " ".join([doc.properties["text"] for doc in retrieved_data])

        # Use a valid Gemini model that supports generateContent (like "gemini-pro" or another)
        model = GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(f"Context: {context}\nUser Query: {query}")

        return response.text if response else "Error generating response."

    except Exception as e:
        logging.error(f"❌ Error generating response: {str(e)}")
        return f"Error processing request: {str(e)}"

import atexit
atexit.register(lambda: client.close() if client else None)  # ✅ Ensure connection closes
