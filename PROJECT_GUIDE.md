# 📘 Corporate Knowledge Nexus — Project Guide

## What Is This?
A fully integrated **RAG + LLM + NLQ** system for corporate knowledge management. Employees upload documents, log daily work, and query an AI that searches documents and databases using plain English.

---

## 🛠 Tech Stack Used

| Layer | Technology | Why |
|:--|:--|:--|
| **Backend Framework** | FastAPI (Python) | Fast, auto-generates `/docs` API explorer |
| **Database (SQL)** | SQLite via SQLAlchemy 2 | Zero-config, easily swapped to PostgreSQL |
| **Data Schema** | Star Schema | `Fact_WorkLog` + 3 Dimension tables |
| **Vector DB** | ChromaDB (persistent) | Stores document embeddings locally |
| **Embeddings + LLM** | OpenAI (`text-embedding-ada-002` + `gpt-4o-mini`) | Best quality RAG pipeline |
| **Auth** | JWT (python-jose) + bcrypt | Stateless, secure tokens |
| **Frontend** | Next.js 16 + TypeScript | File-based routing, SSR-capable |
| **Styling** | Tailwind CSS v4 | Dark glassmorphism design |
| **Deployment** | Docker + Docker Compose | One-command deploy |

---

## 📂 File Structure Explained

```
know_net_pro/
├── START_BACKEND.bat          ← Double-click to start backend (auto-installs)
├── START_FRONTEND.bat         ← Double-click to start frontend
├── docker-compose.yml         ← One-command Docker deployment
│
├── backend/
│   ├── app/
│   │   ├── main.py            ← FastAPI app entry point
│   │   ├── core/
│   │   │   ├── config.py      ← All settings (reads .env)
│   │   │   └── security.py    ← JWT + password hashing
│   │   ├── db/
│   │   │   └── session.py     ← DB engine, session, Base class
│   │   ├── models/
│   │   │   └── models.py      ← The Star Schema (SQLAlchemy ORM)
│   │   ├── schemas/
│   │   │   └── schemas.py     ← Pydantic v2 request/response shapes
│   │   ├── services/
│   │   │   ├── vector_store.py← ChromaDB wrapper
│   │   │   ├── ingestion.py   ← Parses PDF/TXT, chunks, embeds
│   │   │   └── rag.py         ← RAG + Fresher Mode logic
│   │   └── api/
│   │       ├── deps.py        ← JWT auth dependency
│   │       ├── router.py      ← Aggregates all routers
│   │       └── endpoints/
│   │           ├── auth.py    ← POST /register, POST /login
│   │           ├── documents.py← POST /upload, GET /documents/
│   │           ├── worklogs.py ← CRUD + statistics
│   │           ├── projects.py ← CRUD
│   │           └── chat.py    ← POST /chat/ (RAG query)
│   ├── seed.py                ← Creates default admin + sample project
│   ├── requirements.txt       ← Pinned Python dependencies
│   ├── Dockerfile             ← Docker image for backend
│   └── .env.example           ← Copy this to .env and fill in values
│
└── frontend/
    ├── app/
    │   ├── layout.tsx         ← Root layout with AuthProvider
    │   ├── globals.css        ← Global Tailwind + dark theme
    │   ├── page.tsx           ← Redirects to /login or /dashboard
    │   ├── login/page.tsx     ← Login + Register (tabs)
    │   ├── dashboard/page.tsx ← Stats overview + quick actions
    │   ├── chat/page.tsx      ← AI chat with Fresher Mode toggle
    │   ├── upload/page.tsx    ← Upload documents + see library
    │   ├── worklogs/page.tsx  ← Submit + view work log feed
    │   └── projects/page.tsx  ← Create + view projects
    ├── components/
    │   ├── Sidebar.tsx        ← Navigation sidebar
    │   └── AppLayout.tsx      ← Protected layout wrapper
    ├── lib/
    │   ├── api.ts             ← Typed API client for all endpoints
    │   └── auth-context.tsx   ← React auth context (login/logout)
    ├── .env.local             ← Frontend env (API URL)
    └── Dockerfile.frontend    ← Multi-stage Docker build
```

---

## ⚙️ How It Works (Data Flow)

### Document Upload Flow
1. User uploads PDF/TXT from `/upload`
2. Frontend sends `multipart/form-data` to `POST /api/v1/documents/upload`
3. Backend saves file to `./uploaded_docs/`
4. `ingestion.py` extracts text, chunks it, embeds via OpenAI
5. Chunks stored in ChromaDB; metadata saved to `Dim_Document` table

### AI Query Flow (RAG)
1. User types question in `/chat`
2. Frontend calls `POST /api/v1/chat/` with `{ query, fresher_mode }`
3. `rag.py` runs semantic search in ChromaDB (top 4 chunks)
4. Chunks + query sent to `gpt-4o-mini`
5. If **Fresher Mode ON**: system prompt says "explain simply, be encouraging"
6. Answer + source document names returned to UI

### Work Log Flow (Analytics)
1. Employee submits daily standup on `/worklogs`
2. Data saved to `Fact_WorkLog` (linked to `Dim_Employee` + `Dim_Project`)
3. `/worklogs/stats` aggregates for the live Dashboard

---

## 🚀 How to Run

### Option A: Local (Windows) — Quickest
1. Copy `backend/.env.example` → `backend/.env`; fill in `OPENAI_API_KEY`
2. Double-click **`START_BACKEND.bat`**
3. Double-click **`START_FRONTEND.bat`**
4. Open `http://localhost:3000`
5. Login: `admin@company.com` / `admin123`

### Option B: Docker
```bash
cd know_net_pro
docker compose up --build
```

---

## ✅ What Is 100% Complete

- [x] Star Schema database (Employee, Project, Document, WorkLog)
- [x] JWT authentication (register + login)
- [x] Document upload + indexing into ChromaDB
- [x] RAG pipeline with OpenAI GPT-4o-mini
- [x] Fresher Mode for interns
- [x] Work Log submission + live stats on Dashboard
- [x] Project management CRUD
- [x] Full Next.js frontend (6 pages + reusable sidebar)
- [x] Docker + Docker Compose deployment
- [x] One-click startup scripts (Windows .bat)

---

## ⚠️ What YOU Need to Do (Required)

| Task | Why | Where |
|:--|:--|:--|
| **Add OpenAI API Key** | Without it, AI won't answer | `backend/.env` → `OPENAI_API_KEY=sk-...` |
| **Change SECRET_KEY** | Security — never use default in production | `backend/.env` → `SECRET_KEY=...` |
| **Change admin password** | Default `admin123` is unsafe for production | Register a new admin on `/login` |

---

## 🔮 Optional Future Enhancements

| Feature | Description |
|:--|:--|
| PostgreSQL migration | Just change `DATABASE_URL` in `.env` |
| Role-Based Access Control | Restrict docs/projects by department |
| Full Text-to-SQL agent | LangChain SQL Agent for complex analytics |
| Email notifications | Alert authors when documents become stale |
| DOCX support | Add `python-docx`, update `ingestion.py` |
| AWS S3 storage | Replace local file save with `boto3` |
| SSO / Active Directory | Replace JWT with SAML/OAuth |
