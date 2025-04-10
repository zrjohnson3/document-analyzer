// API configuration from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT || 30000);

/**
 * API response types
 */
export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface UploadResponse {
  message: string;
  path: string;
}

export interface AnalysisResponse {
  file: string;
  document_type: string;
  analysis: string;
}

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  type?: string;
}

export interface FilesListResponse {
  files: FileInfo[];
}

export interface GenerateResponse {
  message: string;
  files: {
    docx?: string;
    pdf?: string;
  };
}

/**
 * Create fetch options with timeout
 */
const createFetchOptions = (options: RequestInit = {}): RequestInit => {
  const controller = new AbortController();
  const { signal } = controller;
  
  // Set timeout
  setTimeout(() => controller.abort(), API_TIMEOUT);
  
  return {
    ...options,
    signal,
    headers: {
      ...options.headers,
    },
  };
};

/**
 * Upload a single file to the backend
 */
export async function uploadFile(file: File): Promise<ApiResponse<UploadResponse>> {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload/`, createFetchOptions({
      method: "POST",
      body: formData,
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Upload failed" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Upload failed" };
  }
}

/**
 * Upload multiple files to the backend
 */
export async function uploadMultipleFiles(
  files: File[]
): Promise<ApiResponse<{ message: string; results: Record<string, unknown>[] }>> {
  try {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });

    const response = await fetch(`${API_BASE_URL}/upload/multiple`, createFetchOptions({
      method: "POST",
      body: formData,
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Multiple file upload failed" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Multiple file upload failed" };
  }
}

/**
 * Get a list of all uploaded files
 */
export async function getUploadedFiles(): Promise<ApiResponse<FilesListResponse>> {
  try {
    const response = await fetch(`${API_BASE_URL}/upload/files`, createFetchOptions({
      method: "GET",
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Failed to fetch files" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Failed to fetch files" };
  }
}

/**
 * Delete an uploaded file
 */
export async function deleteUploadedFile(
  filename: string
): Promise<ApiResponse<{ message: string }>> {
  try {
    const response = await fetch(`${API_BASE_URL}/upload/files/${encodeURIComponent(filename)}`, createFetchOptions({
      method: "DELETE",
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Failed to delete file" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Failed to delete file" };
  }
}

/**
 * Preview the contents of a file
 */
export async function previewFile(
  filename: string,
  maxChars: number = 5000
): Promise<ApiResponse<{ filename: string; preview: string; has_more: boolean; total_length: number }>> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/upload/preview/${encodeURIComponent(filename)}?max_chars=${maxChars}`,
      createFetchOptions({
        method: "GET",
      })
    );

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Failed to preview file" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Failed to preview file" };
  }
}

/**
 * Analyze a single document
 */
export async function analyzeDocument(
  filePath: string,
  documentType: string = "general"
): Promise<ApiResponse<AnalysisResponse>> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate/analyze`, createFetchOptions({
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        file_path: filePath,
        document_type: documentType,
      }),
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Analysis failed" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Analysis failed" };
  }
}

/**
 * Generate a master document from multiple input documents
 */
export async function generateDocument(
  filePaths: string[],
  outputType: string = "animal_boarding",
  outputFilename: string = "master_document",
  formats: string[] = ["docx", "pdf"]
): Promise<ApiResponse<GenerateResponse>> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate/generate`, createFetchOptions({
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        file_paths: filePaths,
        output_type: outputType,
        output_filename: outputFilename,
        formats,
      }),
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Document generation failed" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Document generation failed" };
  }
}

/**
 * Get a list of all generated output files
 */
export async function getGeneratedFiles(): Promise<ApiResponse<FilesListResponse>> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate/outputs`, createFetchOptions({
      method: "GET",
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Failed to fetch generated files" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Failed to fetch generated files" };
  }
}

/**
 * Get download URL for a generated file
 */
export function getFileDownloadUrl(filename: string): string {
  return `${API_BASE_URL.replace('/api', '')}/outputs/${encodeURIComponent(filename)}`;
}

/**
 * Delete a generated output file
 */
export async function deleteGeneratedFile(
  filename: string
): Promise<ApiResponse<{ message: string }>> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate/outputs/${encodeURIComponent(filename)}`, createFetchOptions({
      method: "DELETE",
    }));

    if (!response.ok) {
      const errorData = await response.json();
      return { error: errorData.detail || "Failed to delete generated file" };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : "Failed to delete generated file" };
  }
} 