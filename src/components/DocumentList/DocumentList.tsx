import React from "react";
import { FileWithPreview } from "../../types";
import "./DocumentList.css";

/**
 * DocumentList Component Props
 * @property {FileWithPreview[]} documents - Array of uploaded documents with previews
 * @property {Function} onRemove - Callback function to remove a document by ID
 */
interface DocumentListProps {
  documents: FileWithPreview[];
  onRemove: (id: string) => void;
}

/**
 * DocumentList Component
 *
 * Displays a grid of uploaded documents with their names, sizes, and removal options.
 * Shows an empty state when no documents are uploaded.
 */
export const DocumentList: React.FC<DocumentListProps> = ({
  documents,
  onRemove,
}) => {
  // Show empty state when no documents are uploaded
  if (documents.length === 0) {
    return (
      <div className="document-list-empty">
        <p>No documents uploaded yet</p>
        <p>Upload documents to see them here</p>
      </div>
    );
  }

  return (
    <div className="document-list">
      {documents.map((doc) => (
        <div key={doc.id} className="document-item">
          <div className="document-info">
            {/* Document name with overflow handling */}
            <span className="document-name">{doc.file.name}</span>
            {/* Document size in MB with formatted decimal */}
            <span className="document-size">
              {(doc.file.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
          {/* Remove button with confirmation callback */}
          <button className="remove-button" onClick={() => onRemove(doc.id)}>
            Remove
          </button>
        </div>
      ))}
    </div>
  );
};
