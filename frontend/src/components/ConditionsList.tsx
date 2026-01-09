import { cn } from "@/lib/utils";
import { Stethoscope } from "lucide-react";

interface Condition {
  name: string;
  confidence: 'high' | 'medium' | 'low';
  description?: string;
}

interface ConditionsListProps {
  conditions: Condition[];
}

export const ConditionsList = ({ conditions }: ConditionsListProps) => {
  const confidenceStyles = {
    high: "bg-secondary/30 text-secondary-foreground border-secondary/50",
    medium: "bg-accent/50 text-accent-foreground border-accent/60",
    low: "bg-muted text-muted-foreground border-border",
  };

  if (!conditions || conditions.length === 0) {
    return (
      <div className="bg-muted/50 rounded-lg p-5 text-center animate-fade-in">
        <Stethoscope className="w-8 h-8 mx-auto text-muted-foreground mb-2" />
        <p className="text-muted-foreground text-sm">
          No specific conditions are indicated with the current information.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3 animate-fade-in">
      {conditions.map((condition, index) => (
        <div
          key={index}
          className="flex items-start gap-3 p-4 bg-card rounded-lg border border-border"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          <div className="flex-1">
            <div className="flex items-center gap-3 flex-wrap">
              <span className="font-medium text-foreground">
                {condition.name}
              </span>
              <span
                className={cn(
                  "px-2.5 py-0.5 rounded-full text-xs font-medium border",
                  confidenceStyles[condition.confidence]
                )}
              >
                {condition.confidence} confidence
              </span>
            </div>
            {condition.description && (
              <p className="mt-1.5 text-sm text-muted-foreground">
                {condition.description}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
