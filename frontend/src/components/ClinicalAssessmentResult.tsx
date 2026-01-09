import type { ClinicalAssessment } from "@/services/clinicalApi";
import { RiskBadge } from "./RiskBadge";
import { ClinicalExplanation } from "./ClinicalExplanation";
import { EvidenceSection } from "./EvidenceSection";
import { ClinicalSignals } from "./ClinicalSignals";
import { LabResultsTable } from "./LabResultsTable";
import { StructuredSymptoms } from "./StructuredSymptoms";
import { AlertOctagon } from "lucide-react";

interface ClinicalAssessmentResultProps {
  assessment: ClinicalAssessment;
}

export const ClinicalAssessmentResult = ({ assessment }: ClinicalAssessmentResultProps) => {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Risk Level - Most Prominent */}
      <RiskBadge
        level={assessment.risk_level}
        explanation={assessment.triage_rationale}
      />

      {/* Escalation Warning */}
      {assessment.escalation_required && (
        <div className="flex items-center gap-3 p-4 rounded-lg bg-risk-critical/10 border-2 border-risk-critical animate-pulse-slow">
          <AlertOctagon className="w-6 h-6 text-risk-critical flex-shrink-0" />
          <div>
            <span className="font-semibold text-risk-critical">Escalation Required</span>
            <p className="text-sm text-foreground/80 mt-0.5">
              This case requires immediate escalation to senior clinical staff.
            </p>
          </div>
        </div>
      )}

      {/* Structured Symptoms */}
      {assessment.structured_symptoms && (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold font-heading text-foreground">
            Symptom Analysis
          </h3>
          <StructuredSymptoms symptoms={assessment.structured_symptoms} />
        </div>
      )}

      {/* Clinical Signals */}
      {assessment.clinical_signals && (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold font-heading text-foreground">
            Clinical Warning Signals
          </h3>
          <ClinicalSignals signals={assessment.clinical_signals} />
        </div>
      )}

      {/* Lab Results */}
      {assessment.lab_results && assessment.lab_results.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold font-heading text-foreground">
            Laboratory Results
          </h3>
          <LabResultsTable results={assessment.lab_results} />
        </div>
      )}

      {/* Clinical Explanation */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold font-heading text-foreground">
          Triage Rationale
        </h3>
        <ClinicalExplanation explanation={assessment.triage_rationale} />
      </div>

      {/* Evidence & Safety */}
      <EvidenceSection
        evidence={assessment.evidence}
        safetyNotes={assessment.safety_notes}
      />
    </div>
  );
};
