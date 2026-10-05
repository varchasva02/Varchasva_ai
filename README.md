# Varchasva AI 🤖

> A personal AI assistant that answers questions about my projects, skills, experience, and background using Retrieval-Augmented Generation (RAG).

🌐 **Live Demo:** https://varchasva-ai.vercel.app/  
💻 **GitHub:** https://github.com/varchasva02/Varchasva_ai

---

## 📌 Overview

Varchasva AI is a full-stack AI-powered portfolio assistant built to provide visitors with an interactive way to learn about my technical skills, projects, experience, and other portfolio information.

Instead of relying entirely on the language model's general knowledge, the application uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant information from a curated personal knowledge base before generating an answer.

The application is fully deployed with the frontend hosted on **Vercel** and the backend hosted on **Railway**.

---

## ✨ Features

- 🤖 AI-powered conversational portfolio assistant
- 🔎 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic search using Sentence Transformers
- ⚡ FAISS vector similarity search
- 🔤 Hybrid retrieval using semantic similarity, keyword overlap, and intent-based boosting
- 💬 Clean conversational chat interface
- 📝 Markdown-formatted AI responses
- 🔐 Secure server-side Gemini API integration
- 🌐 Fully deployed frontend and backend
- 🟢 Real-time backend health status
- ⏱️ Persistent vector store for production
- 📱 Responsive web interface

---

## 🏗️ Architecture

```text
User / Web
    │
    ▼
React + TypeScript / Vercel
    │
    │ POST /ask
    ▼
Flask + Gunicorn / Railway
    │
    ▼
RAG Retrieval
    │
    ├── Sentence Transformers
    ├── FAISS
    ├── Keyword Overlap
    └── Intent Boosting
    │
    ▼
Retrieved Context
    │
    ▼
Gemini API
    │
    ▼
AI Response
```

---

## 🧠 How the RAG Pipeline Works

1. **User Query** — The user asks a question through the React frontend.
2. **Query Embedding** — The question is converted into a vector using `sentence-transformers/all-MiniLM-L6-v2`.
3. **Vector Search** — FAISS searches the precomputed vector index for relevant knowledge-base chunks.
4. **Hybrid Retrieval** — Semantic similarity, keyword overlap, and query intent are combined to improve retrieval.
5. **Context + Gemini** — Retrieved information is passed to Gemini along with the question to generate the final response.

---

## ⚡ Production Optimization

Initially, the application generated embeddings for the entire knowledge base when the first user request arrived. This caused excessive memory usage in the Railway deployment.

The production implementation instead precomputes and persists the vector store:

```text
rag/
├── faiss_index.bin
└── chunks.json
```

The application loads these artifacts directly at runtime.

```text
Application startup
        ↓
Load existing FAISS index
        ↓
User asks question
        ↓
Embed ONLY the query
        ↓
Search FAISS
        ↓
Retrieve relevant context
        ↓
Generate response
```

This avoids rebuilding the entire vector store during requests and significantly reduces runtime memory usage.

The vector store can be intentionally regenerated locally whenever the underlying knowledge base is updated.

---

## 🖥️ Tech Stack

### Frontend
- React
- TypeScript
- Vite
- CSS
- React Markdown

### Backend
- Python
- Flask
- Gunicorn
- Flask-CORS

### AI / RAG
- Google Gemini API
- Sentence Transformers
- `all-MiniLM-L6-v2`
- FAISS
- PyTorch

### Data Processing
- PyPDF

### Deployment
- Vercel — Frontend
- Railway — Backend
- GitHub — Source Control

---

## 📁 Project Structure

```text
Varchasva_ai/
│
├── data/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
│
├── rag/
│   ├── embedder.py
│   ├── retriever.py
│   ├── vector_store.py
│   ├── pipeline.py
│   ├── faiss_index.bin
│   └── chunks.json
│
├── app.py
├── requirements.txt
├── validate_data.py
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/varchasva02/Varchasva_ai.git
cd Varchasva_ai
```

### 2. Create a Python virtual environment

```bash
python3.12 -m venv .venv
```

Activate it:

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> Never commit `.env` or expose the Gemini API key in the frontend.

---

## ▶️ Run the Backend

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

For production-style local testing:

```bash
gunicorn app:app
```

---

## ▶️ Run the Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Start the development server:

```bash
npm run dev
```

---

## 🔐 Environment Variables

### Backend

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Frontend

```env
VITE_API_URL=http://127.0.0.1:5000
```

For production, `VITE_API_URL` points to the deployed Railway backend.

The Gemini API key is **never stored in the frontend**.

---

## 📡 API

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "online",
  "message": "Varchasva AI API is running"
}
```

### Ask a Question

```http
POST /ask
```

Request:

```json
{
  "question": "What projects has Varchasva built?"
}
```

Response:

```json
{
  "question": "What projects has Varchasva built?",
  "answer": "..."
}
```

---

## 🌐 Deployment

### Frontend

**Vercel:**  
https://varchasva-ai.vercel.app/

### Backend

**Railway:**  
https://varchasvaai-production.up.railway.app/

Production flow:

```text
Vercel
   ↓
Railway
   ↓
FAISS + RAG
   ↓
Gemini
```

---

## 🩺 Backend Health Monitoring

The frontend periodically checks the backend health endpoint.

When the Railway backend is reachable:

```text
🟢 ONLINE
```

If the backend becomes unavailable:

```text
🔴 OFFLINE
```

The health check runs immediately when the application loads and every 30 seconds afterward.

---

## 🚀 Future Improvements

- Expand and better structure the personal knowledge base
- Add richer project-specific information
- Add contact and social profile information
- Improve conversational memory
- Add analytics for commonly asked portfolio questions
- Improve retrieval evaluation and ranking
- Add automated testing for the RAG pipeline

---

## 👨‍💻 Author

**Kumar Varchasva**

AIML Student interested in Artificial Intelligence, Machine Learning, Full-Stack Development, and practical AI applications.

### Connect

- Portfolio / Live Demo: https://varchasva-ai.vercel.app/

---

## ⭐ If you found this project interesting

Feel free to explore the repository, try the live demo, or connect with me.
