import { cn } from "@/lib/utils";
import { FlaskConical, TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { LabResult } from "@/services/clinicalApi";

interface LabResultsTableProps {
  results: LabResult[];
}

export const LabResultsTable = ({ results }: LabResultsTableProps) => {
  if (!results || results.length === 0) {
    return null;
  }

  // Separate critical/used results from others
  const usedForRisk = results.filter(r => r.used_for_risk);
  const otherResults = results.filter(r => !r.used_for_risk);

  const getStatusIcon = (status: string) => {
    const normalizedStatus = status.toLowerCase();
    if (normalizedStatus === 'high') return <TrendingUp className="w-4 h-4 text-risk-critical" />;
    if (normalizedStatus === 'low') return <TrendingDown className="w-4 h-4 text-wisteria" />;
    if (normalizedStatus === 'normal') return <Minus className="w-4 h-4 text-risk-low" />;
    return null;
  };

  const getStatusBadge = (status: string) => {
    const normalizedStatus = status.toLowerCase();
    const styles = {
      high: "bg-risk-critical/20 text-risk-critical border-risk-critical/30",
      low: "bg-wisteria/20 text-wisteria border-wisteria/30",
      normal: "bg-risk-low/20 text-risk-low border-risk-low/30",
      unclassified: "bg-muted text-muted-foreground border-border",
    };
    return styles[normalizedStatus as keyof typeof styles] || styles.unclassified;
  };

  const ResultRow = ({ result }: { result: LabResult }) => (
    <tr className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
      <td className="py-2 px-3">
        <div className="flex items-center gap-2">
          {result.used_for_risk && (
            <span className="w-1.5 h-1.5 rounded-full bg-secondary flex-shrink-0" />
          )}
          <span className="text-sm text-foreground">{result.name}</span>
        </div>
      </td>
      <td className="py-2 px-3 text-right">
        <span className="text-sm font-medium text-foreground">
          {typeof result.value === 'number' ? result.value.toFixed(2) : result.value}
        </span>
        <span className="text-xs text-muted-foreground ml-1">{result.unit}</span>
      </td>
      <td className="py-2 px-3 text-center">
        {result.reference_low !== undefined && result.reference_high !== undefined ? (
          <span className="text-xs text-muted-foreground">
            {result.reference_low} - {result.reference_high}
          </span>
        ) : (
          <span className="text-xs text-muted-foreground">—</span>
        )}
      </td>
      <td className="py-2 px-3">
        <div className="flex items-center justify-end gap-2">
          {getStatusIcon(result.status)}
          <span className={cn(
            "px-2 py-0.5 rounded text-xs font-medium border",
            getStatusBadge(result.status)
          )}>
            {result.status}
          </span>
        </div>
      </td>
    </tr>
  );

  return (
    <div className="space-y-4 animate-fade-in">
      {usedForRisk.length > 0 && (
        <div>
          <h5 className="text-sm font-medium text-foreground mb-2 flex items-center gap-2">
            <FlaskConical className="w-4 h-4 text-secondary" />
            Labs Used for Risk Assessment
          </h5>
          <div className="bg-card rounded-lg border border-border overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="bg-muted/50 text-xs text-muted-foreground">
                  <th className="py-2 px-3 text-left font-medium">Test</th>
                  <th className="py-2 px-3 text-right font-medium">Value</th>
                  <th className="py-2 px-3 text-center font-medium">Reference</th>
                  <th className="py-2 px-3 text-right font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {usedForRisk.map((result, index) => (
                  <ResultRow key={index} result={result} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {otherResults.length > 0 && (
        <details className="group">
          <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2">
            <FlaskConical className="w-4 h-4" />
            All Lab Results ({otherResults.length} tests)
          </summary>
          <div className="mt-2 bg-card rounded-lg border border-border overflow-hidden">
            <div className="max-h-64 overflow-y-auto">
              <table className="w-full">
                <thead className="sticky top-0 bg-muted/80 backdrop-blur">
                  <tr className="text-xs text-muted-foreground">
                    <th className="py-2 px-3 text-left font-medium">Test</th>
                    <th className="py-2 px-3 text-right font-medium">Value</th>
                    <th className="py-2 px-3 text-center font-medium">Reference</th>
                    <th className="py-2 px-3 text-right font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {otherResults.map((result, index) => (
                    <ResultRow key={index} result={result} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </details>
      )}
    </div>
  );
};
