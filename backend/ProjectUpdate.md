# 📘 ClinAssist AI
#### Evidence-Grounded Clinical Decision & Triage Assistant
## 1️⃣ Project Overview
#### Project Name

**ClinAssist AI**

> **One-Line Description**

ClinAssist AI is an evidence-grounded, multi-agent clinical triage assistant that helps healthcare workers assess patient risk and next steps using structured reasoning — without replacing doctors.
___
## 2️⃣ Problem Statement

In many under-resourced and rural regions:

- Healthcare workers are overloaded or lack specialist support
- Early symptoms of serious or rare conditions are often mis-triaged
- Generic AI chatbots hallucinate medical information
- Existing clinical decision systems are expensive and enterprise-only

**Gap:**
There is no affordable, explainable, safety-first AI system that assists clinical reasoning and triage without attempting diagnosis.
___
## 3️⃣ Solution Summary

ClinAssist AI provides decision support, not diagnosis.

It:

- Structures patient symptoms into a clinical schema

- Retrieves relevant medical evidence from trusted sources
- Reasons over possible conditions (not final diagnoses)

- Assigns triage risk (Low / Medium / Critical)

- Recommends next steps and escalation when needed

- Explains why each output was generated

**All outputs are:**

- evidence-grounded

- explainable

- safety-guarded

- human-in-the-loop friendly
___
## 4️⃣ Target Users

**Primary Users**

- Rural healthcare workers

- Junior doctors

- Medical interns

- Community health staff

**Not intended for**

- Direct patient self-diagnosis

- Automated medical decision-making

- Emergency replacement systems
___
## 5️⃣ Core Features (Judge-Relevant)
1. Evidence-Grounded Reasoning

     - Uses Retrieval-Augmented Generation (RAG)

     - Medical sources (WHO, CDC, guidelines)

     - No hallucinated medical claims

2. Multi-Agent Architecture

     - Agentic workflow using LangGraph

     - Each agent has a single, controlled responsibility

3. Differential Possibilities (Not Diagnosis)

     - Outputs “conditions to consider”

     - Avoids legal and ethical risks

4. Triage Intelligence

     - Low / Medium / Critical risk classification

     - Escalation for high-risk cases

5. Explainability

     - Shows which symptoms triggered reasoning

     - Shows which evidence supported outputs

6. Multi-Modal Input (Optional)

     - Text symptoms (primary)

     - Lab report images via OCR (supporting evidence)

7. Responsible AI by Design

     - Explicit disclaimers

     - Safety guardrails

     - Human-in-the-loop escalation
___
## 6️⃣ System Architecture (High Level)
```bash
User Input (Text / Image)
        ↓
Azure Vision OCR (image → text)
        ↓
Symptom Structuring Agent
        ↓
Evidence Retrieval Agent (Qdrant)
        ↓
Reasoning Agent (LLM)
        ↓
Triage Agent
        ↓
Safety Guard Agent
        ↓
Final Output (with explanations & evidence)
```
---
## 7️⃣ Tech Stack (Final & Locked)
**🧠 AI & Reasoning**

- **LLM: NVIDIA NIM (via LangChain OpenAI-compatible wrapper)**

- **Agent Framework: LangGraph**

- **Prompt & RAG Framework: LangChain**

**📚 Retrieval / Knowledge**

- Vector Database: QdrantDB

     Local Docker instance

- Chunking: LangChain text splitters (500–800 tokens)

**🖼 Image Processing**

- OCR: Azure AI Vision (READ only)

     - No captioning

     - No visual reasoning

**⚙ Backend**

- Framework: FastAPI
- Validation: Pydantic
- Language: Python 3.10+

**🎨 Frontend**

- Minimal React / Next.js UI

- Single input form

- Single results view

**🗄 Storage**

- Qdrant → vector + document storage

- SQLite / in-memory → demo logs & cache
___
## 8️⃣ Why This Architecture Was Chosen

| Requirement |	Decision|
|-------------|-------------|
||Safety|	Multi-agent + schema-driven
|Explainability|	RAG + evidence citations
|Cost control|	Local Qdrant, limited OCR
|Reliability|	No fragile cloud dependencies
|Hackathon readiness|	Minimal infra, focused scope
___
## 9️⃣ Multi-Agent Design (LangGraph)
Agents Used

1. Symptom Structuring Agent

      Converts free text into structured clinical shema

2. Evidence Retrieval Agent
     - Queries Qdrant for relevant medical evidence
3. Reasoning Agent
     - Produces possible conditions with eplanations
4. Triage Agent
     - Assigns urgency and risk level
5. safety Guard Agent
     - Enforces disclaimers and escalation rules

___
## 10️⃣ Data Flow Example

1. User enters:

     - Age, gender
     - Symptoms
     - Optional lab report image

2. OCR extracts lab text (if provided)

3. Symptoms + lab text → structured schema

4. Evidence retrieved from medical documents

5. Reasoning agent generates:

     - Possible conditions
     - Supporting symptoms
     - Evidence snippets

6. Triage agent assigns risk

7. Safety guard ensures responsible output
___ 
## 11️⃣ Build Roadmap (0 → Submission)
**Phase 0 – Planning**

- Lock scope
- Lock stack
- Define user and flow

**Phase 1 – Knowledge & RAG**

- Run Qdrant
- Ingest medical documents
- Validate vector retrieval

**Phase 2 – Clinical Schema**

- Define strict input/output schema
- Prevent hallucinations early

**Phase 3 – Agentic Core**

- Implement LangGraph agents
- Wire deterministic flow

**Phase 4 – Backend APIs**

- FastAPI endpoints
- Validation and caching

**Phase 5 – OCR Integration**

- Image → text only
- Merge with symptom data

**Phase 6 – Frontend**

- Minimal, clear UI
- No unnecessary visuals

**Phase 7 – Safety & Ethics**

- Disclaimers
- Escalation logic
- Explainability text

**Phase 8 – Demo Preparation**

- Precomputed demo cases
- Cached responses
- Zero-failure demo

**Phase 9 – Submission**

- Demo video
- README + architecture
- Judge explanation
___
## 12️⃣ Responsible AI Statement

ClinAssist AI:

- Does not provide medical diagnosis
- Does not replace healthcare professionals
- Provides decision support only
- Encourages professional consultation
- Escalates high-risk cases
___
## 13️⃣ Why This Can Win Imagine Cup

Because it demonstrates:

- Real-world relevance
- Engineering maturity
- Ethical AI practices
- Clear problem framing
- Focused execution
- Explainable intelligence

Most teams overbuild.
This system finishes.
___
14️⃣ Project Status

- OCR: ✅ Working
- Vector DB: ⏳ In progress
- Agents: ⏳ In progress
- Backend: ⏳ Planned
- Demo: ⏳ Planned