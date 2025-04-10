import { useState } from "react";
import { FileUpload } from "../components/FileUpload/FileUpload";
import { DocumentList } from "../components/DocumentList/DocumentList";
import { ProgressTracker } from "../components/ProgressTracker/ProgressTracker";
import { FileWithPreview } from "../types";
import { uploadDocuments, generateDocument } from "../services/api";
import "./DocumentUpload.css";

/**
 * Step status types for the progress tracker
 */
type StepStatus = "pending" | "active" | "completed";

/**
 * Step configuration for the progress tracker
 */
interface Step {
  id: number;
  label: string;
  status: StepStatus;
}

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

  // State for tracking processing status
  const [isProcessing, setIsProcessing] = useState(false);
  const [processError, setProcessError] = useState<string | null>(null);

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

  /**
   * Process the uploaded documents
   * Sends the documents to the backend for analysis
   */
  const handleProcessDocuments = async () => {
    if (documents.length === 0) return;

    setIsProcessing(true);
    setProcessError(null);

    try {
      // Create a FormData object to send files
      const formData = new FormData();
      documents.forEach((doc) => {
        // The key must be "files" (matching the parameter name in the backend)
        formData.append("files", doc.file);
      });

      // 1. Upload the documents
      const uploadResult = await uploadDocuments(formData);

      if (uploadResult.error || !uploadResult.data) {
        throw new Error(uploadResult.error || "Failed to upload documents");
      }

      // 2. Generate the document from uploaded file paths
      const generateResult = await generateDocument(
        uploadResult.data,
        "general", // Document type
        "analyzed_document", // Output filename
        ["docx", "pdf"] // Output formats
      );

      if (generateResult.error) {
        throw new Error(generateResult.error);
      }

      // Update the workflow steps
      setCurrentStep(2);
      setSteps((prevSteps) =>
        prevSteps.map((step) =>
          step.id === 2
            ? { ...step, status: "completed" as StepStatus }
            : step.id === 3
            ? { ...step, status: "active" as StepStatus }
            : step
        )
      );

      // Here you would handle the results from the backend
      // For example, storing them in state to display in the next step
      console.log("Generation result:", generateResult.data);
    } catch (error) {
      console.error("Error processing documents:", error);
      setProcessError(
        error instanceof Error
          ? error.message
          : "An error occurred while processing the documents"
      );
    } finally {
      setIsProcessing(false);
    }
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
        <DocumentList
          documents={documents}
          onRemove={handleRemoveDocument}
          onProcess={handleProcessDocuments}
        />

        {/* Processing status message */}
        {isProcessing && (
          <div className="processing-status">
            <p>Processing your documents... This may take a minute.</p>
          </div>
        )}

        {/* Error message if processing fails */}
        {processError && (
          <div className="processing-error">
            <p>Error: {processError}</p>
            <button onClick={() => setProcessError(null)}>Dismiss</button>
          </div>
        )}
      </div>
    </div>
  );
};
