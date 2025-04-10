/**
 * File with Preview Interface
 * 
 * Represents an uploaded file with:
 * @property {File} file - The actual File object from the browser
 * @property {string} preview - Object URL for preview purposes
 * @property {string} id - Unique identifier for tracking
 */
export interface FileWithPreview {
  file: File;
  preview: string;
  id: string;
} 