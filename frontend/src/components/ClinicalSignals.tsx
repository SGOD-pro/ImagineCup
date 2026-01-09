import { AlertCircle, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ClinicalSignals as ClinicalSignalsType } from "@/services/clinicalApi";

interface ClinicalSignalsProps {
  signals: ClinicalSignalsType;
}

const signalLabels: Record<keyof ClinicalSignalsType, string> = {
  red_flag_present: "Red Flag Present",
  bleeding_present: "Bleeding Present",
  neurological_symptoms: "Neurological Symptoms",
  respiratory_distress: "Respiratory Distress",
  persistent_fever: "Persistent Fever",
  severe_pain: "Severe Pain",
  anemia: "Anemia",
  severe_anemia: "Severe Anemia",
  thrombocytopenia: "Thrombocytopenia",
  severe_thrombocytopenia: "Severe Thrombocytopenia",
  thrombocytosis: "Thrombocytosis",
  microcytosis: "Microcytosis",
  macrocytosis: "Macrocytosis",
  leukopenia: "Leukopenia",
  leukocytosis: "Leukocytosis",
  guideline_early_warning: "Early Warning (Guideline)",
  guideline_severity: "Severity (Guideline)",
  guideline_escalation: "Escalation (Guideline)",
  physiological_instability: "Physiological Instability",
  hematologic_abnormality: "Hematologic Abnormality",
  infection_like_pattern: "Infection-like Pattern",
};

export const ClinicalSignals = ({ signals }: ClinicalSignalsProps) => {
  const activeSignals = Object.entries(signals).filter(([_, value]) => value === true);
  const inactiveSignals = Object.entries(signals).filter(([_, value]) => value === false);

  if (activeSignals.length === 0) {
    return (
      <div className="bg-muted/30 rounded-lg p-4 text-center">
        <CheckCircle2 className="w-6 h-6 mx-auto text-risk-low mb-2" />
        <p className="text-sm text-muted-foreground">No clinical warning signals detected</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Active Warning Signals */}
      <div>
        <h5 className="text-sm font-medium text-foreground mb-2 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-risk-medium" />
          Active Warning Signals ({activeSignals.length})
        </h5>
        <div className="flex flex-wrap gap-2">
          {activeSignals.map(([key]) => (
            <span
              key={key}
              className={cn(
                "px-2.5 py-1 rounded-full text-xs font-medium",
                "bg-risk-medium/20 text-risk-medium border border-risk-medium/30"
              )}
            >
              {signalLabels[key as keyof ClinicalSignalsType] || key}
            </span>
          ))}
        </div>
      </div>

      {/* Inactive Signals (collapsed view) */}
      <details className="text-sm">
        <summary className="cursor-pointer text-muted-foreground hover:text-foreground transition-colors">
          Show all signals ({inactiveSignals.length} clear)
        </summary>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {inactiveSignals.map(([key]) => (
            <span
              key={key}
              className="px-2 py-0.5 rounded-full text-xs bg-muted text-muted-foreground"
            >
              {signalLabels[key as keyof ClinicalSignalsType] || key}
            </span>
          ))}
        </div>
      </details>
    </div>
  );
};
