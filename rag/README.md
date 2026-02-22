# 🧠 Retrieval-Augmented Generation (RAG) Module  
**Hack-For-Green-Bharat**

This module implements the **Retrieval-Augmented Generation (RAG) layer** for the *Streaming RAG-Based Environmental Intelligence System*.

It is responsible for transforming regulatory documents and environmental standards into a **live, searchable knowledge base**, enabling the LLM to generate **grounded, context-aware, and up-to-date environmental explanations**.

---

## 👤 Ownership & Role Alignment

**Owner:** Aditi Tiwari  
**Role:** RAG + LLM Systems Engineer

This module fulfills the following responsibilities from the team role assignment:

- Build and maintain a live document knowledge base  
- Implement semantic chunking and embedding generation  
- Perform vector similarity retrieval  
- Integrate LLM safely (no hallucination, no guessing)  
- Provide context-aware answers using live data + documents  
- Ensure demo-safe and explainable outputs  

---

## 🧩 How This Fits Into the Overall System

```text
[ Live Environmental Data Stream ]
                ↓
      Streaming Module
                ↓
      RAG Module  ←── YOU OWN THIS
                ↓
     LLM Explanation Engine
                ↓
     Alerts / API / Dashboard
```
```text
rag/
├── docs/
│   ├── aqi_health_impacts.txt
│   ├── aqi_india_rules.txt
│   ├── aqi_pollutants_and_measurement.txt
│   └── aqi_thresholds_simple.txt
│
├── chunk_docs.py
├── embed_docs.py
├── vector_search.py
├── llm_answer.py
└── README.md
```
File-by-File Breakdown
🔹 docs/

Purpose:
Stores environmental regulatory documents and AQI standards.

Why it exists:

Acts as external knowledge source

Keeps LLM grounded in verified standards

Allows easy updates without retraining models

🔹 chunk_docs.py

Purpose:
Splits large documents into smaller semantic chunks.

Why it exists:

Improves retrieval precision

Prevents context overload

Enables fine-grained similarity matching

Role Mapping:

Document ingestion

Knowledge base preparation

🔹 embed_docs.py

Purpose:
Converts document chunks into vector embeddings using:

sentence-transformers

all-MiniLM-L6-v2

Output:

Each chunk → 384-dimensional vector

Role Mapping:

Semantic encoding

Vector store creation

🔹 vector_search.py

Purpose:
Performs cosine similarity search between:

User query embedding

Stored document embeddings

Process:

Question → embedding

Compare with document vectors

Retrieve top-k most relevant chunks

Role Mapping:

Retrieval engine

Context selection layer

🔹 llm_answer.py

Purpose:
Generates grounded answers using retrieved context.

Safety Rules Enforced:

Answer ONLY using provided context

Do NOT guess

Do NOT add external facts

If answer not found → respond with insufficient data

Role Mapping:

Safe LLM integration
```text
Context-aware reasoning
Regulatory Documents
        ↓
chunk_docs.py
        ↓
embed_docs.py
        ↓
Vector Store
        ↓
User Question
        ↓
vector_search.py
        ↓
Retrieved Context
        ↓
llm_answer.py
        ↓
Grounded Environmental Explanation
```
🛡 Safety Design

This module prevents hallucination by:

Strict prompt engineering

Retrieval-first generation

No direct free-form answering

Enforcing conservative outputs

The LLM cannot answer outside retrieved context.

🔌 Integration Contracts
🔹 For Streaming Team

Can inject live AQI values into prompt

No need to handle regulatory logic

🔹 For Backend/API Team

Can expose answer_question() as endpoint

Stateless and reusable

🔹 For Dashboard Team

Can display:

AQI severity explanations

Health advisories

Regulatory category mappings
