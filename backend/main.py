# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from embed import store_in_weaviate
from chat import generate_response
from scrape import scrape_url

# Load environment variables
load_dotenv()

# Setup Logging
LOG_DIRECTORY = "backend/logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "app.log")
os.makedirs(LOG_DIRECTORY, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "Welcome to RAG Chatbot API!"}

@app.post("/scrape/")
def scrape_and_store(request: ScrapeRequest):
    try:
        content = scrape_url(request.url)
        if not content:
            raise HTTPException(status_code=500, detail="Failed to scrape content")
        store_in_weaviate(request.url, content)
        return {"message": "Content scraped and stored successfully"}
    except Exception as e:
        logging.error(f"Scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/")
def chat(request: ChatRequest):
    try:
        response = generate_response(request.query)
        return {"answer": response}
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
