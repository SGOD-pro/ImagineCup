from langchain_community.document_loaders import PyPDFLoader
from app.ai.llm import NvidiaLLM
from time import sleep
import os
import json





import ast

def parse_llm_output(raw):
    """
    Handles:
    - Proper JSON
    - Python dict string (single quotes)
    """
    if isinstance(raw, dict):
        return raw

    text = raw.strip()

    # Try JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(text)
    except Exception:
        return None
pdf_files = [
    # {"name": "HIVTB_Clinical_Guide_Primary_Care 2018_March2021_en.pdf", "page": 199},
    # {"name": "JBDS_02_DKA_Guideline_with_QR_code_March_2023.pdf", "page": 12},
    {"name": "KDIGO-2024-CKD-Guideline.pdf", "page": 2},
    {"name": "NONCOMMUNICABLE (PEN).pdf", "page": 2},
    {"name": "Operational-Manual-for-Tuberculosis_compressed.pdf", "page": 0},
    {"name": "pneumonia-diagnosis-and-management-pdf-66144010347205.pdf", "page": 0},
    {"name": "Prevention and treatment of.pdf", "page": 0},
    {
        "name": "Surviving-Sepsis-Campaign_International-Guidelines-for-Management-of-Sepsis-and-Septic-Shock-2021.pdf",
        "page": 0
    },
    {"name": "WHO malaria guidelines - August 2025.pdf", "page": 0},
]


os.makedirs("extracted_data", exist_ok=True)

for items in pdf_files:
    pdf=items["name"]
    INPUT_FILE= pdf
    
    OUTPUT_FILE = f"extracted_data/{pdf.replace('.pdf', '.json')}"



    file_path = f"./Pdfs/{INPUT_FILE}"
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    new_docs=[]


    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            new_docs = json.load(f)
    else:
        new_docs = []
    
    for doc in range(items["page"],12):
        if len((str(docs[doc].page_content)))<100:
            continue
        model= NvidiaLLM(model_name="meta/llama-3.2-1b-instruct",temp=.4).model
        # model= NvidiaLLM(model_name="google/gemma-3-1b-it",temp=.15).model
        res=model.invoke(input=f'''You are a STRICT clinical guideline filter for a medical triage system.

    YOUR ROLE:
    You are NOT a summarizer.
    You are NOT an explainer.
    You are a GATEKEEPER.

    Your only job is to decide whether the given text contains
    EXPLICIT, PATIENT-LEVEL CLINICAL DECISION INFORMATION
    that affects triage or severity assessment for an individual patient.

    ────────────────────────────────
    STEP 1 — DECIDE KEEP OR DISCARD
    ────────────────────────────────

    KEEP the text ONLY IF it contains AT LEAST ONE sentence that EXPLICITLY
    states a patient-level clinical rule such as:

    - early warning signs or danger signs
    - severity classification or disease progression
    - criteria that distinguish non-severe vs severe disease
    - escalation, referral, or triage decisions
    - symptom-based suspicion rules
    - patient-level risk factors (e.g., pregnancy, age, comorbidities)
    - explicit progression from mild → severe disease

    The sentence MUST directly change a clinician’s triage decision
    for an individual patient.

    ────────────────────────────────
    HARD DISQUALIFIERS — IMMEDIATE DISCARD
    ────────────────────────────────

    If the text is primarily about ANY of the following,
    you MUST DISCARD, even if it mentions disease names:

    - epidemiology, prevalence, case counts, fatality rates
    - geography, regions, countries, climate, seasonality
    - circulating serotypes or strains
    - outbreak reports or historical outbreaks
    - transmission patterns or vectors
    - public health strategies, surveillance, prevention programs
    - policy, governance, resolutions, or regulations
    - treatment protocols, medications, dosages, or procedures
    - references, citations, figures, tables, or charts

    IMPORTANT CLARIFICATIONS:

    - Acute fever ALONE is NOT an early warning sign.
    - Disease presence ALONE is NOT clinical decision logic.
    - Epidemiology is NEVER a patient-level risk factor.
    - Geographic or demographic information is NEVER a risk factor.
    - Do NOT infer or interpret. Only accept EXPLICIT statements.

    If you cannot point to an EXPLICIT patient-level triage rule,
    you MUST DISCARD.

    ────────────────────────────────
    STEP 2 — EXTRACTION (ONLY IF KEEP = TRUE)
    ────────────────────────────────

    If KEEP = TRUE:

    - Extract ONLY the sentences that describe
    clinical classification, severity, progression, or triage decisions.
    - IGNORE and EXCLUDE all background, epidemiology, and context.
    - Rewrite concisely in neutral clinical language.
    - Do NOT invent information.
    - Do NOT include statistics, regions, or populations.

    ────────────────────────────────
    MANDATORY SELF-CHECK
    ────────────────────────────────

    Before producing output, ask yourself:

    “Does this extracted text change a clinician’s triage decision
    for an individual patient RIGHT NOW?”

    If the answer is NO → OUTPUT keep:false.

    ────────────────────────────────
    OUTPUT FORMAT — STRICT JSON ONLY
    ────────────────────────────────

    Your output MUST be valid JSON and MUST match this schema EXACTLY.

    If USEFUL:{

    {"keep": "True",
    "category": ["severity", "early_warning", "escalation"],
    "extracted_text": "<explicit patient-level clinical decision text only>"}
        }
    ---------
    //Rules(Use only 1 or 2 not all):

    early_warning → symptoms before shock
    severity → severe / non-severe distinction
    escalation → admit / refer / ICU
    ---------
    If NOT useful:
    { {"keep": "False",
    "category": [],
    "extracted_text": "Null"}}


    Strictly NO texts, only json output's.
    Strictly NO explanations.
    Strictly NO markdown.

    TEXT:
    <<<{docs[doc]}>>>
    ''')
        # print(docs[doc])
        print(res.content)
        try:
            res_json = parse_llm_output(res.content)
            if not res_json:
                continue

            keep = res_json.get("keep", False)
            if isinstance(keep, str):
                keep = keep.lower() == "true"

            if not keep:
                continue

            extracted = res_json.get("extracted_text")
            if not extracted or extracted == "Null":
                continue
            
            docs[doc].page_content=extracted
            t=docs[doc]
            new_docs.append({
                "metadata": t.metadata,
                "text": extracted,
                "category": res_json.get("category", [])
            })
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(new_docs, f, indent=2, ensure_ascii=False)
            print(doc)
            print(pdf)
        except Exception as e:
            print(e)
            break

        sleep(2)


# import os
# import json

# os.makedirs("extracted_data", exist_ok=True)

# with open("extracted_data/DENGUE2.json", "w", encoding="utf-8") as f:
#     json.dump(new_docs, f, indent=2, ensure_ascii=False)




# from langchain_text_splitters import RecursiveCharacterTextSplitter

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=512, chunk_overlap=100, add_start_index=True
# )
# all_splits = text_splitter.split_documents(docs)

# print(len(all_splits))