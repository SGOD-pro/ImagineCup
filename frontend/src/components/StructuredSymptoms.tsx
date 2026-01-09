import { AlertTriangle, Stethoscope } from "lucide-react";
import type { StructuredSymptoms as StructuredSymptomsType } from "@/services/clinicalApi";

interface StructuredSymptomsProps {
  symptoms: StructuredSymptomsType;
}

export const StructuredSymptoms = ({ symptoms }: StructuredSymptomsProps) => {
  if (!symptoms) return null;

  return (
    <div className="space-y-3 animate-fade-in">
      {/* Chief Complaints */}
      {symptoms.chief_complaints && symptoms.chief_complaints.length > 0 && (
        <div>
          <h5 className="text-sm font-medium text-foreground mb-2 flex items-center gap-2">
            <Stethoscope className="w-4 h-4 text-secondary" />
            Chief Complaints
          </h5>
          <div className="flex flex-wrap gap-2">
            {symptoms.chief_complaints.map((complaint, index) => (
              <span
                key={index}
                className="px-3 py-1 rounded-full text-sm bg-secondary/20 text-secondary-foreground border border-secondary/30"
              >
                {complaint}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Red Flags */}
      {symptoms.red_flags && symptoms.red_flags.length > 0 && (
        <div>
          <h5 className="text-sm font-medium text-foreground mb-2 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-risk-medium" />
            Red Flags Identified
          </h5>
          <div className="space-y-2">
            {symptoms.red_flags.map((flag, index) => (
              <div
                key={index}
                className="flex items-start gap-2 p-2 rounded-lg bg-risk-medium/10 border border-risk-medium/20"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-risk-medium mt-2 flex-shrink-0" />
                <span className="text-sm text-foreground">{flag}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Duration & Severity */}
      {(symptoms.duration || symptoms.severity) && (
        <div className="flex gap-4 text-sm">
          {symptoms.duration && (
            <div>
              <span className="text-muted-foreground">Duration: </span>
              <span className="text-foreground font-medium">{symptoms.duration}</span>
            </div>
          )}
          {symptoms.severity && (
            <div>
              <span className="text-muted-foreground">Severity: </span>
              <span className="text-foreground font-medium">{symptoms.severity}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
