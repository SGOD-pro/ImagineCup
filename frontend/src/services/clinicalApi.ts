// API service for ClinAssist AI backend integration

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

interface FormInput {
  user_symptoms: string;
  context: {
    age: number;
    sex: string;
  };
}

interface LabData {
  name: string;
  value: number;
  unit: string;
  status: string;
  used_for_risk: boolean;
  note: string;
}

interface OcrText {
  source: string;
  full_text: string;
}

export interface NormalizedLabData extends FormInput {
  labs: LabData[];
}

export interface StructuredSymptoms {
  chief_complaints: string[];
  duration: string | null;
  severity: string | null;
  red_flags: string[];
}

export interface Hypothesis {
  condition: string;
  confidence: 'high' | 'medium' | 'low';
  description?: string;
}
export interface LabFlag {
  value: number;
  low: number;
  high: number;
  status: string;
}
export interface LabResult {
  name: string;
  value: number | string;
  unit: string;
  status: string;
  used_for_risk: boolean;
  note?: string;
  reference_low?: number;
  reference_high?: number;
}

export interface Evidence {
  statement: string;
  signal_type: string;
  symptoms: string[];
  source: string;
  page: number;
  score: number;
}
export interface ClinicalSignals {
  red_flag_present: boolean;
  bleeding_present: boolean;
  neurological_symptoms: boolean;
  respiratory_distress: boolean;
  persistent_fever: boolean;
  severe_pain: boolean;
  anemia: boolean;
  severe_anemia: boolean;
  thrombocytopenia: boolean;
  severe_thrombocytopenia: boolean;
  thrombocytosis: boolean;
  microcytosis: boolean;
  macrocytosis: boolean;
  leukopenia: boolean;
  leukocytosis: boolean;
  guideline_early_warning: boolean;
  guideline_severity: boolean;
  guideline_escalation: boolean;
  physiological_instability: boolean;
  hematologic_abnormality: boolean;
  infection_like_pattern: boolean;
}
export interface ClinicalAssessment {
  raw_symptoms_text: string;
  patient_age: number;
  patient_gender: string;
  lab_results: LabResult[];
  structured_symptoms: StructuredSymptoms;
  evidence: Evidence[];
  clinical_signals: ClinicalSignals;
  lab_flags: Record<string, LabFlag>;
  reasoning_summary: {
    high_confidence: Hypothesis[];
    medium_confidence: Hypothesis[];
  };
  hypotheses: Hypothesis[];
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  triage_rationale: string;
  escalation_required: boolean;
  safety_notes: string;
}


export interface UploadResponse {
  status: string;
  blob_ids: string[];
}

export interface OcrResponse {
  ocr_texts: OcrText[];
}

interface OCRNormalization extends FormInput {
  ocr_texts: OcrText[];
}

export interface ApiError {
  message: string;
  code?: string;
}

class ClinicalApiService {
  private async request<T>(endpoint: string, options: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
      },
    });
    console.log(response);
    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ message: "An error occurred" }));
      throw new Error(
        error.message || `Request failed with status ${response.status}`
      );
    }

    return response.json();
  }

  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    return this.request<UploadResponse>("/clinical/upload", {
      method: "POST",
      body: formData,
    });
  }

  async performOcr(blob_ids: string[]): Promise<OcrResponse> {
    return this.request<OcrResponse>("/clinical/ocr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ blob_ids }),
    });
  }

  async normalizeOcrData(ocr: OCRNormalization): Promise<NormalizedLabData> {
    return this.request<NormalizedLabData>("/clinical/ocr-normalization", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify( ocr ),
    });
  }

  async analyzeCase(data: NormalizedLabData): Promise<ClinicalAssessment> {
    return this.request<ClinicalAssessment>("/clinical/analyze-case", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }

  // Orchestrated flow - single entry point for the UI (supports multiple files)
  async processCase(
    age: number,
    gender: string,
    symptoms: string,
    labFiles: File[],
    onProgress?: (step: string) => void
  ): Promise<ClinicalAssessment> {
    let combinedLabData: NormalizedLabData = {
      user_symptoms:symptoms,
      context: { age, sex: gender },
      labs: [],
    };

    if (labFiles && labFiles.length > 0) {
      const allTests: NormalizedLabData["labs"] = [];
      console.log("Processing lab files...",labFiles.length);
      for (let i = 0; i < labFiles.length; i++) {
        const file = labFiles[i];
        onProgress?.(`Processing file ${i + 1} of ${labFiles.length}...`);

        const uploadResult = await this.uploadFile(file);

        onProgress?.(`Running OCR on ${file.name}...`);
        const ocrResult = await this.performOcr(uploadResult.blob_ids);

        onProgress?.(`Extracting lab values from ${file.name}...`);
        const labData = await this.normalizeOcrData({
          ocr_texts: ocrResult.ocr_texts,
          user_symptoms:symptoms,
          context: { age, sex:gender },
        });

        allTests.push(...labData.labs);
      }

      if (allTests.length > 0) {
        combinedLabData.labs = allTests;
      }
    }

    onProgress?.("Analyzing case...");
    const assessment = await this.analyzeCase(combinedLabData);
    console.log("Final Assessment",assessment);
    return assessment;
  }

  async getHealthCheck(): Promise<string> {
    return this.request<string>("/health", { method: "GET" });
  }
}

export const clinicalApi = new ClinicalApiService();
