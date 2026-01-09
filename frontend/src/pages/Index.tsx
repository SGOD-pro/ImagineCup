import { useCallback, useEffect, useState } from "react";
import { PatientForm } from "@/components/PatientForm";
import { ClinicalAssessmentResult } from "@/components/ClinicalAssessmentResult";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { ThemeToggle } from "@/components/ThemeToggle";
import { clinicalApi, type ClinicalAssessment } from "@/services/clinicalApi";
import { Activity, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState("");
  const [assessment, setAssessment] = useState<ClinicalAssessment | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (data: {
    age: number;
    gender: string;
    symptoms: string;
    labFiles: File[];
  }) => {
    setIsLoading(true);
    setError(null);
    setAssessment(null);
    console.log(data);
    try {
      const result = await clinicalApi.processCase(
        data.age,
        data.gender,
        data.symptoms,
        data.labFiles,
        (step) => setLoadingMessage(step)
      );
      setAssessment(result);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "An unexpected error occurred";
      setError(message);
      toast({
        title: "Analysis Failed",
        description: message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
      setLoadingMessage("");
    }
  };

  const handleReset = () => {
    setAssessment(null);
    setError(null);
  };
  useCallback(async() => {
      try {
        const res=await clinicalApi.getHealthCheck();
      } catch (error) {
        toast({
          title: "Error",
          description: "Health check failed",
          variant: "destructive",
        });
      }
  }, []);
  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-md sticky top-0 z-10 transition-colors">
        <div className="container max-w-3xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cool-sky to-wisteria flex items-center justify-center shadow-clinical">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold font-heading text-foreground">
                  ClinAssist AI
                </h1>
                <p className="text-xs text-muted-foreground">
                  Clinical Decision Support
                </p>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-3xl mx-auto px-4 py-8">
        {/* Patient Input Section */}
        <section className="clinical-card p-6 mb-8 transition-colors">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold font-heading text-foreground">
              Patient Information
            </h2>
            {assessment && (
              <Button
                variant="ghost"
                size="sm"
                onClick={handleReset}
                className="text-muted-foreground hover:text-foreground"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                New Assessment
              </Button>
            )}
          </div>

          <PatientForm onSubmit={handleSubmit} isLoading={isLoading} />
        </section>

        {/* Loading State */}
        {isLoading && (
          <section className="clinical-card p-6 mb-8 transition-colors">
            <LoadingSpinner message={loadingMessage} />
          </section>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <section className="clinical-card p-6 mb-8 border-destructive/50 bg-destructive/5 animate-fade-in transition-colors">
            <div className="text-center">
              <p className="text-destructive font-medium">
                Unable to complete analysis
              </p>
              <p className="text-sm text-muted-foreground mt-1">{error}</p>
            </div>
          </section>
        )}

        {/* Clinical Assessment Results */}
        {assessment && !isLoading && (
          <section className="clinical-card p-6 transition-colors">
            <h2 className="text-lg font-semibold font-heading text-foreground mb-6">
              Clinical Assessment
            </h2>
            <ClinicalAssessmentResult assessment={assessment} />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-6 mt-auto transition-colors">
        <div className="container max-w-3xl mx-auto px-4">
          <p className="text-center text-xs text-muted-foreground">
            ClinAssist AI provides clinical decision support only. All
            assessments must be verified by qualified healthcare professionals.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
