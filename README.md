# Wikipedia Chatbot

A full-stack Retrieval-Augmented Generation (RAG) chatbot that answers user questions using Wikipedia articles as context.

Built using:

* React.js
* Tailwind CSS
* Flask
* LangChain
* FAISS
* Groq LLM API

---

## Features

* Multi-query Wikipedia retrieval
* Retrieval-Augmented Generation (RAG)
* Semantic search using embeddings
* FAISS vector search
* Modern React + Tailwind chat UI
* Flask backend API
* Context-aware answers
* Section-based document chunking
* MMR (Max Marginal Relevance) retrieval

---

## Tech Stack

### Frontend

* React.js
* Vite
* Tailwind CSS

### Backend

* Flask
* LangChain
* FAISS
* HuggingFace Embeddings
* Groq API
* Wikipedia API

---

## Project Structure

```
wikipedia-chatbot/
│
├── .gitignore
│
├── backend/
│   ├── .venv/
│   ├── .env
│   ├── app.py
│   ├── backend.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    └── vite.config.js
```

---

## How It Works

1. User asks a question from the React frontend
2. Flask API receives the query
3. LangChain generates multiple search queries
4. Relevant Wikipedia articles are retrieved
5. Articles are chunked and embedded
6. FAISS performs semantic retrieval
7. Retrieved context is sent to the LLM
8. Final response is generated and returned

---

## Backend Setup

### 1. Navigate to backend

```bash
cd backend
```

### 2. Create virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Inside `backend/.env`:

```env
GROQ_API_KEY=your_api_key_here
TURNSTILE_SECRET_KEY=your_turnstile_secret_key_here
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
RATE_LIMIT_PER_MINUTE=5
RATE_LIMIT_PER_DAY_PER_IP=20
GLOBAL_DAILY_CAP=200
```

### 5. Run Flask server

```bash
python app.py
```

Backend runs on:

```bash
http://127.0.0.1:5000
```

---

## Frontend Setup

### 1. Navigate to frontend

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Run frontend

Create `frontend/.env`:

```env
VITE_API_BASE_URL=
VITE_TURNSTILE_SITE_KEY=your_turnstile_site_key_here
```

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## Environment Variables

| Variable | Description |
| -------- | ----------- |
| `GROQ_API_KEY` | Groq API key |
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile secret for backend verification |
| `ALLOWED_ORIGINS` | Comma-separated frontend origins allowed to call `/chat` |
| `RATE_LIMIT_PER_MINUTE` | Per-IP requests allowed each minute |
| `RATE_LIMIT_PER_DAY_PER_IP` | Per-IP requests allowed per day |
| `GLOBAL_DAILY_CAP` | Global successful chat requests allowed per day |
| `VITE_API_BASE_URL` | Frontend API base URL. Leave empty when nginx serves frontend and backend from the same domain |
| `VITE_TURNSTILE_SITE_KEY` | Cloudflare Turnstile site key used by the frontend |

---

## Public Demo Protection

This app now supports:

* IP-based rate limiting
* Per-IP daily usage caps
* Global daily usage caps
* Cloudflare Turnstile bot protection

If you deploy with nginx, make sure it forwards the client IP so rate limiting works correctly:

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Real-IP $remote_addr;
```

---

## Future Improvements

* Streaming responses
* Persistent FAISS index
* Conversation memory
* Markdown rendering
* Source citations
* Authentication
* Chat history
* Docker deployment
* Async retrieval
* Wikipedia caching
* Vector database persistence

---

## Known Limitations

* FAISS index rebuilds on every query
* Wikipedia retrieval can occasionally fail
* No persistent memory yet
* Response latency can increase for complex queries

---

## Example Questions

* Who invented the transistor?
* Explain the theory of relativity
* What caused World War I?
* How does a neural network work?
* Tell me about the Apollo missions

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

* LangChain
* HuggingFace
* Groq
* Wikipedia API
* FAISS
* React
* Tailwind CSS
