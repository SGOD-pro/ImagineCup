import { FileText } from "lucide-react";

interface ClinicalExplanationProps {
  explanation: string;
}

export const ClinicalExplanation = ({ explanation }: ClinicalExplanationProps) => {
  return (
    <div className="bg-muted/30 rounded-lg p-5 border border-border animate-fade-in">
      <div className="flex items-start gap-3">
        <FileText className="w-5 h-5 text-secondary flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-medium text-foreground mb-2">Clinical Assessment</h4>
          <p className="text-foreground/80 leading-relaxed text-sm">
            {explanation}
          </p>
        </div>
      </div>
    </div>
  );
};
