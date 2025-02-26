# RAG Chatbot Project

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot powered by **Weaviate** for vector database management and **Gemini AI** for natural language processing. The system can scrape content from URLs, generate embeddings, store them in Weaviate, and respond to queries based on context retrieved from the database.

## Features

- **Scraping Content**: Extracts visible content from a provided URL.
- **Weaviate Integration**: Stores the scraped content and its embeddings in a Weaviate vector database.
- **Chatbot**: Uses Gemini AI to generate responses based on the stored data.
- **Dynamic Collection**: Ensures the collection for scraped data exists or creates one dynamically.
- **Logging**: Logs actions for debugging and auditing purposes.

## Technologies Used

- **FastAPI**: Web framework for building the API.
- **Weaviate**: Vector database for storing and querying embeddings.
- **Gemini API**: AI model for generating responses.
- **Sentence-Transformers**: Open-source model for generating embeddings.
- **BeautifulSoup**: Library for web scraping.
- **Requests**: HTTP library for fetching webpage content.

## Project Structure

```bash
backend/
├── embed.py            # Handles Weaviate connection, embedding generation, and storage.
├── scrape.py           # Web scraping logic for fetching visible content from URLs.
├── chat.py             # Handles query processing and response generation.
├── main.py             # FastAPI app that integrates scraping, embedding storage, and chatbot functionalities.
├── logs/               # Log files for scraping, embedding, and server activities.
├── .env                # Configuration file with environment variables (API keys, URLs, etc.)
└── requirements.txt    # List of project dependencies.
Setup Instructions
Follow these steps to set up and run the RAG Chatbot project:

1. Clone the Repository
bash
Copy
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
2. Set Up the Environment
Create a virtual environment for the project:

bash
Copy
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
3. Install Dependencies
Install the required dependencies:

bash
Copy
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory with the following keys:

plaintext
Copy
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro  # Update with a valid model from the ListModels API
WEAVIATE_URL=https://your-weaviate-instance-url
WEAVIATE_API_KEY=your_weaviate_api_key
Make sure to replace your_gemini_api_key and your_weaviate_api_key with your actual API keys.

5. Start the Application
Run the FastAPI server:

bash
Copy
uvicorn main:app --reload
The application will now be running at http://127.0.0.1:8000.

API Endpoints
1. /
GET: Test if the server is running.

Response:

json
Copy
{
  "message": "Welcome to RAG Chatbot API!"
}
2. /scrape/
POST: Scrapes content from the provided URL and stores it in Weaviate.

Request:

json
Copy
{
  "url": "https://example.com"
}
Response:

json
Copy
{
  "message": "Content scraped and stored successfully"
}
If scraping fails:

json
Copy
{
  "error": "Failed to scrape content"
}
3. /chat/
POST: Generates a chatbot response based on the query and context retrieved from Weaviate.

Request:

json
Copy
{
  "query": "What is the weather like today?"
}
Response:

json
Copy
{
  "answer": "The weather today is sunny with a chance of rain in the evening."
}
Logging
Logs are stored in the backend/logs/ directory.
You can check scrape.log for scraping-related logs and app.log for general application logs.
Troubleshooting
Error with Weaviate: Ensure your Weaviate instance is running and properly configured in the .env file.
Gemini API Errors: Ensure your Gemini API key is valid, and the selected model supports the generateContent method.
Conclusion
This project demonstrates how to build a Retrieval-Augmented Generation (RAG) chatbot using Weaviate and Gemini API. The system allows users to scrape web content, store embeddings in Weaviate, and generate AI-driven responses based on the scraped data.

Front end:

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
