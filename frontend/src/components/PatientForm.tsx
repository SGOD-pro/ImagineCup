import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Activity } from "lucide-react";
import { FileUploader } from "@/components/FileUploader";

interface PatientFormProps {
  onSubmit: (data: {
    age: number;
    gender: string;
    symptoms: string;
    labFiles?: File[];
  }) => void;
  isLoading: boolean;
}

export const PatientForm = ({ onSubmit, isLoading }: PatientFormProps) => {
  const [age, setAge] = useState<string>("");
  const [gender, setGender] = useState<string>("");
  const [symptoms, setSymptoms] = useState<string>("");
  const [labFiles, setLabFiles] = useState<File[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!age || !gender || !symptoms.trim()) return;
  
    onSubmit({
      age: parseInt(age, 10),
      gender,
      symptoms: symptoms.trim(),
      labFiles: labFiles.length > 0 ? labFiles : undefined,
    });
  };

  const handleFilesReady = useCallback((files: File[]) => {
    setLabFiles(files);
  }, []);

  const isValid = age && gender && symptoms.trim();

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Age */}
        <div className="space-y-2">
          <Label htmlFor="age" className="text-sm font-medium text-foreground">
            Patient Age
          </Label>
          <Input
            id="age"
            type="number"
            min="0"
            max="150"
            placeholder="Enter age"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            className="clinical-input h-11"
            disabled={isLoading}
          />
        </div>

        {/* Gender */}
        <div className="space-y-2">
          <Label htmlFor="gender" className="text-sm font-medium text-foreground">
            Gender
          </Label>
          <Select value={gender} onValueChange={setGender} disabled={isLoading}>
            <SelectTrigger className="clinical-input h-11">
              <SelectValue placeholder="Select gender" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="male">Male</SelectItem>
              <SelectItem value="female">Female</SelectItem>
              <SelectItem value="other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Symptoms */}
      <div className="space-y-2">
        <Label htmlFor="symptoms" className="text-sm font-medium text-foreground">
          Presenting Symptoms
        </Label>
        <Textarea
          id="symptoms"
          placeholder="Describe the patient's symptoms, chief complaints, and relevant history..."
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          className="clinical-input min-h-[140px] resize-none"
          disabled={isLoading}
        />
      </div>

      {/* Lab Report Upload */}
      <div className="space-y-2">
        <Label className="text-sm font-medium text-foreground">
          Lab Reports <span className="text-muted-foreground font-normal">(Optional)</span>
        </Label>
        <FileUploader
          onFilesReady={handleFilesReady}
          disabled={isLoading}
          maxFiles={5}
        />
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        disabled={!isValid || isLoading}
        className="w-full h-12 bg-gradient-to-r from-cool-sky to-wisteria hover:from-cool-sky/90 hover:to-wisteria/90 text-white font-semibold text-base shadow-clinical transition-all duration-300 hover:shadow-clinical-lg disabled:opacity-50"
      >
        <Activity className="w-5 h-5 mr-2" />
        {isLoading ? "Processing..." : "Analyze Case"}
      </Button>
    </form>
  );
};
