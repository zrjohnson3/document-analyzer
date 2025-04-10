import { useState, useCallback } from "react";
import { FileWithPreview } from "../../types";
import "./FileUpload.css";

/**
 * FileUpload Component Props
 * @property {Function} onFilesSelected - Callback function when files are selected
 * @property {string[]} acceptedFileTypes - List of accepted file extensions
 * @property {number} maxFileSize - Maximum file size in bytes
 */
interface FileUploadProps {
  onFilesSelected: (files: FileWithPreview[]) => void;
  acceptedFileTypes?: string[];
  maxFileSize?: number; // in bytes
}

/**
 * FileUpload Component
 *
 * Provides a drag and drop interface for uploading documents.
 * Handles file validation for type and size, and generates previews.
 */
export const FileUpload: React.FC<FileUploadProps> = ({
  onFilesSelected,
  acceptedFileTypes = [".pdf", ".docx"],
  maxFileSize = 10 * 1024 * 1024, // 10MB default
}) => {
  // State to track if user is currently dragging files over the dropzone
  const [isDragging, setIsDragging] = useState(false);

  /**
   * Handle dragover event - updates state to show active drop area
   */
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  /**
   * Handle dragleave event - resets drop area state
   */
  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  /**
   * Handle file drop event - processes dropped files
   */
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
  }, []);

  /**
   * Handle manual file selection through file input
   */
  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files ? Array.from(e.target.files) : [];
      processFiles(files);
    },
    []
  );

  /**
   * Process files by:
   * 1. Filtering by valid types and sizes
   * 2. Creating object URLs for previews
   * 3. Generating unique IDs
   * 4. Sending to parent component
   */
  const processFiles = (files: File[]) => {
    const processedFiles = files
      .filter((file) => {
        // Validate file type
        const isValidType = acceptedFileTypes.some((type) =>
          file.name.toLowerCase().endsWith(type)
        );
        // Validate file size
        const isValidSize = file.size <= maxFileSize;
        return isValidType && isValidSize;
      })
      .map((file) => ({
        file,
        preview: URL.createObjectURL(file), // Create preview URL
        id: crypto.randomUUID(), // Generate unique ID
      }));

    onFilesSelected(processedFiles);
  };

  return (
    <div
      className={`upload-zone ${isDragging ? "dragging" : ""}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {/* Hidden file input triggered by clicking the dropzone */}
      <input
        type="file"
        multiple
        accept={acceptedFileTypes.join(",")}
        onChange={handleFileInput}
        className="file-input"
      />
      <div className="upload-content">
        <div className="upload-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        <p>Drag and drop files here or click to select</p>
        <p className="file-types">
          Accepted files: {acceptedFileTypes.join(", ")}
        </p>
        <p className="file-size">
          Max file size: {maxFileSize / (1024 * 1024)}MB
        </p>
      </div>
    </div>
  );
};
