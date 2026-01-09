import { Loader2 } from "lucide-react";

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner = ({ message = "Processing..." }: LoadingSpinnerProps) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      <div className="relative">
        <div className="w-16 h-16 rounded-full bg-primary/20" />
        <Loader2 className="absolute inset-0 m-auto w-10 h-10 text-secondary animate-spin-slow" />
      </div>
      <p className="mt-4 text-muted-foreground font-medium">{message}</p>
    </div>
  );
};
