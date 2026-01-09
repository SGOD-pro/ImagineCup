import { useState, useRef, useCallback, useEffect } from "react";
import { Upload, X, FileText, Image, CheckCircle, AlertCircle } from "lucide-react";
import { Progress } from "@/components/ui/progress";

export interface UploadedFile {
  id: string;
  file: File;
  progress: number;
  status: "pending" | "uploading" | "complete" | "error";
  preview?: string;
  errorMessage?: string;
}

interface FileUploaderProps {
  onFilesReady: (files: File[]) => void;
  disabled?: boolean;
  maxFiles?: number;
}

const CHUNK_SIZE = 256 * 1024; // 256KB chunks

export const FileUploader = ({ onFilesReady, disabled, maxFiles = 5 }: FileUploaderProps) => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const generateId = () => Math.random().toString(36).substring(2, 9);

  const getFilePreview = (file: File): Promise<string | undefined> => {
    return new Promise((resolve) => {
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = () => resolve(undefined);
        reader.readAsDataURL(file);
      } else if (file.type === "application/pdf") {
        resolve("pdf");
      } else {
        resolve(undefined);
      }
    });
  };

  const simulateChunkedUpload = async (fileEntry: UploadedFile) => {
    const totalChunks = Math.ceil(fileEntry.file.size / CHUNK_SIZE);
    
    for (let i = 0; i < totalChunks; i++) {
      await new Promise((resolve) => setTimeout(resolve, 50 + Math.random() * 100));
      
      const progress = Math.min(((i + 1) / totalChunks) * 100, 100);
      
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === fileEntry.id
            ? { ...f, progress, status: progress === 100 ? "complete" : "uploading" }
            : f
        )
      );
    }
  };

  const processFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const validTypes = ["application/pdf", "image/png", "image/jpeg", "image/jpg"];
    
    const validFiles = fileArray.filter((file) => validTypes.includes(file.type));
    
    if (validFiles.length === 0) return;

    const availableSlots = maxFiles - uploadedFiles.length;
    const filesToAdd = validFiles.slice(0, availableSlots);

    const newFileEntries: UploadedFile[] = await Promise.all(
      filesToAdd.map(async (file) => ({
        id: generateId(),
        file,
        progress: 0,
        status: "pending" as const,
        preview: await getFilePreview(file),
      }))
    );

    setUploadedFiles((prev) => [...prev, ...newFileEntries]);

    // Start uploading each file
    for (const entry of newFileEntries) {
      setUploadedFiles((prev) =>
        prev.map((f) => (f.id === entry.id ? { ...f, status: "uploading" } : f))
      );
      await simulateChunkedUpload(entry);
    }
  }, [maxFiles, uploadedFiles.length]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processFiles(e.target.files);
      e.target.value = "";
    }
  };

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      if (!disabled && e.dataTransfer.files.length > 0) {
        processFiles(e.dataTransfer.files);
      }
    },
    [disabled, processFiles]
  );
  const removeFile = (id: string) => {
    setUploadedFiles((prev) => {
      const file = prev.find((f) => f.id === id);
      if (file?.preview && file.preview !== "pdf") {
        URL.revokeObjectURL(file.preview);
      }
      return prev.filter((f) => f.id !== id);
    });
  };
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };



  // Notify parent when files are ready
  useEffect(() => {
    const completedFiles = uploadedFiles
      .filter((f) => f.status === "complete")
      .map((f) => f.file);
    onFilesReady(completedFiles);
  }, [uploadedFiles, onFilesReady]);

  const allComplete = uploadedFiles.length > 0 && uploadedFiles.every((f) => f.status === "complete");

  return (
    <div className="space-y-3">
      {/* Drop Zone */}
      <div
        onClick={() => !disabled && fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-xl p-6
          flex flex-col items-center justify-center gap-2
          transition-all duration-300 cursor-pointer
          ${isDragging 
            ? "border-dragonfruit bg-dragonfruit/10 scale-[1.02]" 
            : "border-border hover:border-cool-sky hover:bg-muted/50"
          }
          ${disabled ? "opacity-50 cursor-not-allowed" : ""}
          ${uploadedFiles.length >= maxFiles ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        <div className={`
          w-12 h-12 rounded-full flex items-center justify-center
          transition-all duration-300
          ${isDragging ? "bg-dragonfruit/20" : "bg-muted"}
        `}>
          <Upload className={`w-6 h-6 transition-colors ${isDragging ? "text-dragonfruit" : "text-muted-foreground"}`} />
        </div>
        <p className="text-sm text-muted-foreground text-center">
          <span className="font-medium text-foreground">Click to upload</span> or drag and drop
        </p>
        <p className="text-xs text-muted-foreground/70">
          PDF, PNG, JPG (max {maxFiles} files)
        </p>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          multiple
          onChange={handleFileChange}
          className="hidden"
          disabled={disabled || uploadedFiles.length >= maxFiles}
        />
      </div>

      {/* File List with Progress */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2 animate-fade-in">
          {uploadedFiles.map((file) => (
            <div
              key={file.id}
              className="group relative bg-card border border-border rounded-lg p-3 transition-all hover:shadow-clinical"
            >
              <div className="flex items-center gap-3">
                {/* Preview */}
                <div className="w-12 h-12 rounded-lg overflow-hidden flex-shrink-0 bg-muted flex items-center justify-center">
                  {file.preview === "pdf" ? (
                    <FileText className="w-6 h-6 text-dragonfruit" />
                  ) : file.preview ? (
                    <img
                      src={file.preview}
                      alt={file.file.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <Image className="w-6 h-6 text-muted-foreground" />
                  )}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">
                    {file.file.name}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <p className="text-xs text-muted-foreground">
                      {(file.file.size / 1024).toFixed(1)} KB
                    </p>
                    {file.status === "complete" && (
                      <span className="flex items-center gap-1 text-xs text-risk-low-foreground bg-risk-low px-1.5 py-0.5 rounded-full">
                        <CheckCircle className="w-3 h-3" />
                        Ready
                      </span>
                    )}
                    {file.status === "error" && (
                      <span className="flex items-center gap-1 text-xs text-destructive">
                        <AlertCircle className="w-3 h-3" />
                        Error
                      </span>
                    )}
                  </div>
                  
                  {/* Progress Bar */}
                  {(file.status === "uploading" || file.status === "pending") && (
                    <div className="mt-2">
                      <Progress 
                        value={file.progress} 
                        className="h-1.5 bg-muted"
                      />
                    </div>
                  )}
                </div>

                {/* Percentage */}
                {file.status === "uploading" && (
                  <span className="text-sm font-medium text-cool-sky tabular-nums">
                    {Math.round(file.progress)}%
                  </span>
                )}

                {/* Remove Button */}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(file.id);
                  }}
                  disabled={disabled}
                  className="p-1.5 rounded-full hover:bg-muted transition-colors opacity-0 group-hover:opacity-100"
                >
                  <X className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Summary */}
      {allComplete && uploadedFiles.length > 0 && (
        <p className="text-xs text-center text-muted-foreground animate-fade-in">
          {uploadedFiles.length} file{uploadedFiles.length > 1 ? "s" : ""} ready for analysis
        </p>
      )}
    </div>
  );
};
