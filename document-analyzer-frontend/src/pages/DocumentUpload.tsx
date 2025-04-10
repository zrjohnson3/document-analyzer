import { useState } from "react";
import { FileUpload } from "../components/FileUpload/FileUpload";
import { DocumentList } from "../components/DocumentList/DocumentList";
import { ProgressTracker } from "../components/ProgressTracker/ProgressTracker";
import { FileWithPreview } from "../types";
import "./DocumentUpload.css";

/**
 * Step status types for the progress tracker
 */
type StepStatus = "pending" | "active" | "completed";

/**
 * Step data structure for document processing workflow
 */
type Step = {
  id: number;
  label: string;
  status: StepStatus;
};

/**
 * DocumentUpload Page Component
 *
 * Main application page that handles:
 * 1. Document uploading via drag and drop
 * 2. Listing uploaded documents
 * 3. Tracking the document analysis workflow progress
 *
 * This component integrates multiple sub-components and manages the overall state
 * of the document analysis process.
 */
export const DocumentUpload = () => {
  // State for uploaded documents with previews
  const [documents, setDocuments] = useState<FileWithPreview[]>([]);

  // Current step in the workflow (0-based index)
  const [currentStep, setCurrentStep] = useState(0);

  // Workflow steps configuration
  const [steps, setSteps] = useState<Step[]>([
    { id: 1, label: "Upload Documents", status: "active" },
    { id: 2, label: "Process Documents", status: "pending" },
    { id: 3, label: "Review Results", status: "pending" },
    { id: 4, label: "Generate Output", status: "pending" },
  ]);

  /**
   * Handle newly selected files
   * Updates document list and advances workflow if needed
   *
   * @param newFiles - Array of new files with previews
   */
  const handleFilesSelected = (newFiles: FileWithPreview[]) => {
    // Add new files to existing documents
    setDocuments((prev) => [...prev, ...newFiles]);

    // Advance to the next step if this is the first file and we're on step 0
    if (newFiles.length > 0 && currentStep === 0) {
      setCurrentStep(1);
      // Update step statuses
      setSteps((prevSteps) =>
        prevSteps.map((step) =>
          step.id === 1
            ? { ...step, status: "completed" as StepStatus }
            : step.id === 2
            ? { ...step, status: "active" as StepStatus }
            : step
        )
      );
    }
  };

  /**
   * Handle document removal by ID
   * Cleans up preview URLs and updates workflow state if needed
   *
   * @param id - Document unique identifier
   */
  const handleRemoveDocument = (id: string) => {
    setDocuments((prev) => {
      // Filter out the document to be removed
      const filtered = prev.filter((doc) => doc.id !== id);

      // Clean up preview URLs to prevent memory leaks
      prev
        .filter((doc) => doc.id === id)
        .forEach((doc) => URL.revokeObjectURL(doc.preview));

      // Reset to first step if all documents are removed
      if (filtered.length === 0) {
        setCurrentStep(0);
        setSteps((prevSteps) =>
          prevSteps.map((step) =>
            step.id === 1
              ? { ...step, status: "active" as StepStatus }
              : { ...step, status: "pending" as StepStatus }
          )
        );
      }

      return filtered;
    });
  };

  return (
    <div className="document-upload-page">
      {/* Page header */}
      <h1 className="page-title">Document Analyzer</h1>
      <p className="page-subtitle">
        Upload and analyze your emergency management documents
      </p>

      {/* Progress tracking component */}
      <ProgressTracker steps={steps} currentStep={currentStep} />

      {/* Document upload section */}
      <div className="upload-section">
        <h2 className="section-title">Upload Documents</h2>
        <FileUpload
          onFilesSelected={handleFilesSelected}
          acceptedFileTypes={[".pdf", ".docx"]}
          maxFileSize={20 * 1024 * 1024} // 20MB
        />
      </div>

      {/* Document list section */}
      <div className="documents-section">
        <h2 className="section-title">Uploaded Documents</h2>
        <DocumentList documents={documents} onRemove={handleRemoveDocument} />
      </div>
    </div>
  );
};
