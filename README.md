# ClinAssist AI

**Evidence-Grounded Clinical Decision & Triage Assistant (MVP)**

ClinAssist AI is a safety-first, evidence-grounded clinical decision support system designed to assist healthcare workers with **patient triage and next-step guidance**. The system explicitly **does not provide medical diagnosis** and **does not replace clinicians**.

This repository contains an **architecture-first MVP** built to demonstrate controlled reasoning, evidence separation, and responsible AI practices in healthcare.

---

## 🎯 One-Line Pitch

> ClinAssist AI helps healthcare workers assess risk and decide next clinical steps using explainable, evidence-grounded AI — without replacing doctors.

---

## 🚨 Important Disclaimer (Read First)

ClinAssist AI is **not a medical device**.

* ❌ Not for diagnosis
* ❌ Not for automated medical decision-making
* ❌ Not for patient self-use
* ✅ For clinical **decision support only**
* ✅ Intended for healthcare workers and supervised environments

All outputs are advisory and must be interpreted by qualified professionals.

---

## ❓ Problem Statement

In under-resourced or high-load clinical settings:

* Healthcare workers lack specialist decision support
* Early warning signs are frequently mis-triaged
* General-purpose AI chatbots hallucinate medical facts
* Existing clinical decision systems are expensive and inaccessible

**Gap:** There is no affordable, explainable, safety-first AI system for clinical triage and next-step guidance.

---

## 💡 Solution Overview

ClinAssist AI provides **decision support, not diagnosis**.

It:

* Structures free-text symptoms into clinical signals
* Retrieves trusted medical evidence (guidelines)
* Reasons over *possible conditions* (non-diagnostic)
* Assigns triage risk (Low / Medium / Critical)
* Recommends next steps and escalation
* Explains which signals and evidence were used

---

## 🧠 System Architecture

ClinAssist AI is built as a **multi-agent pipeline** with strict responsibility separation.

```
User Input (Text / Lab Report)
        ↓
Symptom Structuring Agent
        ↓
Evidence Retrieval Agent
        ↓
Reasoning Agent
        ↓
Triage Agent
        ↓
Safety Guard Agent
        ↓
Final Output (Explainable, Non-Diagnostic)
```

### Key Design Properties

* Deterministic agent flow
* Evidence ≠ diagnosis
* Signal-bounded reasoning
* Language restraint enforced
* Human-in-the-loop by design

---

## 🤖 Agents (LangGraph)

| Agent               | Responsibility                                     |
| ------------------- | -------------------------------------------------- |
| Symptom Structuring | Converts raw text into structured clinical signals |
| Evidence Retrieval  | Retrieves relevant guideline evidence              |
| Reasoning           | Generates possible conditions (non-diagnostic)     |
| Triage              | Assigns urgency and risk level                     |
| Safety Guard        | Enforces disclaimers, restraint, escalation        |

Each agent has a **single, controlled responsibility**.

---

## 🧩 Tech Stack (MVP Implementation)

### AI & Reasoning

* LLM: **NVIDIA NIM API**
* Agent orchestration: LangGraph

### Backend

* FastAPI (Python)

### Document & Evidence Handling

* OCR: Azure Vision (text extraction only)
* Storage: Azure Blob Storage

### Frontend

* React
* Tailwind CSS

### Design Note

The system is **provider-agnostic**. The LLM backend can be swapped without affecting safety, reasoning flow, or triage behavior.

---

## 🔐 Responsible AI & Safety

ClinAssist AI enforces safety through **architecture**, not prompt tricks:

* No diagnosis claims
* Non-alarmist language
* Explicit disclaimers
* High-risk escalation
* Evidence-grounded reasoning
* Explainable outputs

Safety rules are applied at multiple stages of the pipeline.

---

## ⚠️ MVP Limitations (Intentional)

This project is an MVP focused on **architecture correctness**, not clinical hardening.

### Known Limitations

* Partial guardrail enforcement
* Frontend signal-gating still being tightened
* Language calibration ongoing

### Identified Example

* A guideline severity signal may be rendered in the UI despite being inactive in backend signals (frontend gating issue).

### Important Note

These limitations **do not affect**:

* Evidence separation
* Reasoning correctness
* Triage logic

---

## 📚 Data Scope & Constraints

ClinAssist AI intentionally uses **limited, curated data**.

### Current Data Usage

* Authoritative medical guidelines only
* Small curated document set
* Limited lab report examples
* No patient history datasets

### Rationale

> In medical AI, incorrect scale is more dangerous than limited scope.

The MVP validates reasoning and safety before data scaling.

---

## 🔎 Evidence ≠ Diagnosis (Core Safety Principle)

* Retrieved evidence may include serious conditions
* Evidence **does not automatically influence** hypotheses or triage
* Only clinical signals trigger reasoning and risk assignment

This prevents signal inflation and diagnostic overreach.

---

## 👤 Target Users

* Rural healthcare workers
* Junior doctors
* Medical interns
* Community health staff

**Not intended for:**

* Patient self-diagnosis
* Autonomous medical decision systems

---

## 🚀 Running the Project (MVP)

> *Exact commands may vary by environment.*

### Backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
npm install
npm run dev
```

Ensure environment variables are set for OCR, storage, and LLM access.

---

## 🧪 Demo Notes

* Use cached demo cases to avoid latency
* Prefer synthetic or anonymized lab reports
* Do not demonstrate diagnosis wording
* Emphasize explainability and restraint

---

## 🏁 Project Status

* Architecture: ✅ Finalized
* OCR Integration: ✅ Working
* Agent Pipeline: ⏳ In Progress
* Frontend Guardrails: ⏳ Tightening
* Demo: ✅ Prepared

---

## 📌 Final Note

ClinAssist AI demonstrates how generative AI can be used **responsibly** in healthcare — with restraint, explainability, and respect for clinical judgment.

Most systems chase scale.

This system proves safety first.
