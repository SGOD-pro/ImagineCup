import { cn } from "@/lib/utils";
import { AlertTriangle, CheckCircle, AlertOctagon } from "lucide-react";

interface RiskBadgeProps {
  level: 'low' | 'medium' | 'high' | 'critical';
  explanation?: string;
}

export const RiskBadge = ({ level, explanation }: RiskBadgeProps) => {
  const normalizedLevel = level.toLowerCase() as 'low' | 'medium' | 'high' | 'critical';
  
  const config = {
    low: {
      icon: CheckCircle,
      label: "LOW RISK",
      className: "risk-badge-low",
      borderColor: "border-risk-low",
    },
    medium: {
      icon: AlertTriangle,
      label: "MEDIUM RISK",
      className: "risk-badge-medium",
      borderColor: "border-risk-medium",
    },
    high: {
      icon: AlertOctagon,
      label: "HIGH RISK",
      className: "risk-badge-critical",
      borderColor: "border-risk-critical",
    },
    critical: {
      icon: AlertOctagon,
      label: "CRITICAL",
      className: "risk-badge-critical",
      borderColor: "border-risk-critical",
    },
  };

  const { icon: Icon, label, className, borderColor } = config[normalizedLevel] || config.medium;

  return (
    <div className={cn("rounded-xl p-6 border-2 animate-fade-in", className, borderColor)}>
      <div className="flex items-center gap-4">
        <Icon className="w-10 h-10 flex-shrink-0" />
        <div>
          <h3 className="text-2xl font-bold font-heading tracking-tight">
            {label}
          </h3>
          {explanation && (
            <p className="mt-1 text-sm opacity-90">{explanation}</p>
          )}
        </div>
      </div>
    </div>
  );
};
