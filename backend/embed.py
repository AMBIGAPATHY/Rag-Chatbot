# backend/embed.py

import os
import logging
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google.generativeai import configure, embed_content

# Load environment variables
load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro-embedding")

# Configure Gemini
configure(api_key=GEMINI_API_KEY)

# ✅ Load Open-Source Transformer Model
local_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # ✅ 384-dimension vector

# Logging
LOG_FILE = "backend/logs/app.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

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

# ✅ Ensure Weaviate Collection Exists
def ensure_weaviate_collection():
    """Ensure Weaviate collection is dynamically created."""
    if not client:
        logging.error("Weaviate connection is not available.")
        return

    try:
        existing_collections = client.collections.list_all()  # ✅ Correct API method (list of strings)

        if "ScrapedData" not in existing_collections:
            client.collections.create(
                name="ScrapedData",
                properties=[
                    {"name": "url", "dataType": ["string"]},
                    {"name": "text", "dataType": ["text"]},
                ],
                vector_index_config={"vectorSize": 384},  # ✅ Ensure vector size matches model
            )
            logging.info("✅ Weaviate Collection Created Dynamically")
        else:
            logging.info("✅ Weaviate Collection Already Exists")

    except Exception as e:
        logging.error(f"❌ Error ensuring collection: {str(e)}")

ensure_weaviate_collection()

# ✅ Generate Embeddings
def generate_embedding(text):
    """Generate embeddings using an open-source transformer model, fallback to Gemini API."""
    try:
        logging.info("🔄 Generating Local Embeddings...")
        embedding = local_model.encode(text).tolist()
        logging.info("✅ Local Embeddings Generated Successfully!")
        return embedding
    except Exception as e:
        logging.warning(f"⚠️ Local embedding failed: {str(e)}. Falling back to Gemini API.")
        try:
            response = embed_content(model=GEMINI_MODEL, content=text, task_type="retrieval_query")
            return response["embedding"]
        except Exception as e:
            logging.error(f"❌ Failed to generate embeddings: {str(e)}")
            return None

# ✅ Store in Weaviate
def store_in_weaviate(url, text):
    """Store embeddings in Weaviate."""
    if not client:
        logging.error("Weaviate connection is not available.")
        return

    try:
        embedding = generate_embedding(text)
        if embedding and len(embedding) == 384:  # ✅ Ensure correct vector size
            client.collections.get("ScrapedData").data.insert(
                properties={"url": url, "text": text}, vector=embedding
            )
            logging.info(f"✅ Stored text for {url} in Weaviate")
        else:
            logging.error(f"❌ Embedding size mismatch: Expected 384, got {len(embedding) if embedding else 'None'}")

    except Exception as e:
        logging.error(f"❌ Failed to store data in Weaviate: {str(e)}")

import atexit
atexit.register(lambda: client.close() if client else None)  # ✅ Ensure connection closes
