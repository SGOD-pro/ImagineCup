import { useState } from "react";
import { ChevronDown, BookOpen, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Evidence } from "@/services/clinicalApi";

interface EvidenceSectionProps {
  evidence: Evidence[];
  safetyNotes: string;
}

export const EvidenceSection = ({ evidence, safetyNotes }: EvidenceSectionProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border border-border rounded-lg overflow-hidden animate-fade-in">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 text-left hover:bg-muted/50 transition-colors"
      >
        <span className="font-medium text-foreground flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-secondary" />
          Evidence & Safety Information
        </span>
        <ChevronDown
          className={cn(
            "w-5 h-5 text-muted-foreground transition-transform duration-200",
            isOpen && "rotate-180"
          )}
        />
      </button>

      <div
        className={cn(
          "overflow-hidden transition-all duration-300",
          isOpen ? "max-h-[800px] opacity-100" : "max-h-0 opacity-0"
        )}
      >
        <div className="p-4 pt-0 space-y-5">
          {/* Evidence Sources */}
          {evidence && evidence.length > 0 && (
            <div>
              <h5 className="text-sm font-medium text-foreground mb-3">
                Reference Sources
              </h5>
              <div className="space-y-3">
                {evidence.slice(0, 5).map((item, index) => (
                  <div
                    key={index}
                    className="p-3 bg-muted/30 rounded-lg border border-border"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span className="px-2 py-0.5 rounded text-xs font-medium bg-secondary/20 text-secondary-foreground">
                        {item.source}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        Page {item.page}
                      </span>
                      <span className="text-xs text-muted-foreground ml-auto">
                        Relevance: {(item.score * 100).toFixed(0)}%
                      </span>
                    </div>
                    {item.symptoms && item.symptoms.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-2">
                        {item.symptoms.map((symptom, idx) => (
                          <span
                            key={idx}
                            className="px-1.5 py-0.5 rounded text-xs bg-accent/30 text-accent-foreground"
                          >
                            {symptom}
                          </span>
                        ))}
                      </div>
                    )}
                    <p className="text-xs text-muted-foreground line-clamp-3">
                      {item.statement}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Safety Notes */}
          <div className="bg-accent/20 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <ShieldAlert className="w-5 h-5 text-accent-foreground flex-shrink-0 mt-0.5" />
              <div>
                <h5 className="text-sm font-medium text-foreground mb-2">
                  Safety Disclaimer
                </h5>
                <p className="text-sm text-muted-foreground">
                  {safetyNotes || "This system provides clinical decision support only and does not diagnose. All assessments should be verified by qualified healthcare professionals."}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
