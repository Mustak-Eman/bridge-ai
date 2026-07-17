"use client";

import {
  ChangeEvent,
  DragEvent,
  useRef,
  useState,
} from "react";

import { FilePreview } from "@/components/documents/file-preview";
import { Button } from "@/components/ui/button";
import { ErrorAlert } from "@/components/ui/error-alert";
import { analyzeDocument } from "@/lib/api/documents";
import { getErrorMessage } from "@/lib/get-error-message";
import type { DocumentAnalysisResponse } from "@/types/api";

interface DocumentUploadPanelProps {
  projectId: string;
  onAnalysisComplete: (analysis: DocumentAnalysisResponse) => void;
  onConnectionChange: (isConnected: boolean) => void;
}

const ALLOWED_EXTENSIONS = [".txt", ".md", ".markdown", ".pdf"];
const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024;

function getFileExtension(filename: string): string {
  const dotIndex = filename.lastIndexOf(".");

  if (dotIndex === -1) {
    return "";
  }

  return filename.slice(dotIndex).toLowerCase();
}

function validateFile(file: File): string | null {
  const extension = getFileExtension(file.name);

  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    return "Choose a TXT, Markdown, or PDF document.";
  }

  if (file.size === 0) {
    return "The selected file is empty.";
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "The selected file must be 10 MB or smaller.";
  }

  return null;
}

export function DocumentUploadPanel({
  projectId,
  onAnalysisComplete,
  onConnectionChange,
}: DocumentUploadPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  function selectFile(file: File) {
    const validationError = validateFile(file);

    if (validationError) {
      setSelectedFile(null);
      setErrorMessage(validationError);
      return;
    }

    setSelectedFile(file);
    setErrorMessage(null);
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (file) {
      selectFile(file);
    }

    event.target.value = "";
  }

  function handleDragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(true);
  }

  function handleDragLeave(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      selectFile(file);
    }
  }

  async function handleAnalyze() {
    if (!selectedFile) {
      setErrorMessage("Select a document before starting analysis.");
      return;
    }

    setIsAnalyzing(true);
    setErrorMessage(null);

    try {
      const analysis = await analyzeDocument(selectedFile);

      onAnalysisComplete(analysis);
      onConnectionChange(true);
    } catch (error) {
      setErrorMessage(getErrorMessage(error));
      onConnectionChange(false);
    } finally {
      setIsAnalyzing(false);
    }
  }

  function handleRemoveFile() {
    setSelectedFile(null);
    setErrorMessage(null);
  }

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-[var(--shadow-sm)]">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
        Document analysis
      </p>

      <h2 className="mt-2 text-xl font-semibold tracking-tight text-[var(--foreground)]">
        Upload operational source material
      </h2>

      <p className="mt-3 text-sm leading-6 text-[var(--foreground-muted)]">
        Upload a policy, program guide, service document, or internal procedure
        for structured analysis.
      </p>

      <div className="mt-6 rounded-lg bg-[var(--surface-subtle)] px-3 py-2 text-xs text-[var(--foreground-muted)]">
        Active project:{" "}
        <span className="font-mono font-semibold text-[var(--foreground)]">
          {projectId}
        </span>
      </div>

      {errorMessage ? (
        <div className="mt-5">
          <ErrorAlert
            title="Document request failed"
            message={errorMessage}
            onDismiss={() => setErrorMessage(null)}
          />
        </div>
      ) : null}

      <input
        ref={inputRef}
        type="file"
        accept=".txt,.md,.markdown,.pdf,text/plain,text/markdown,application/pdf"
        disabled={isAnalyzing}
        onChange={handleInputChange}
        className="hidden"
      />

      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            inputRef.current?.click();
          }
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={[
          "mt-5 flex min-h-48 cursor-pointer flex-col items-center justify-center",
          "rounded-xl border-2 border-dashed px-6 py-8 text-center transition-colors",
          isDragging
            ? "border-[var(--primary)] bg-[var(--primary-subtle)]"
            : "border-[var(--border-strong)] bg-[var(--surface-subtle)] hover:border-[var(--primary)]",
          isAnalyzing ? "pointer-events-none opacity-60" : "",
        ].join(" ")}
      >
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white text-xl shadow-[var(--shadow-sm)]">
          ↑
        </div>

        <p className="mt-4 text-sm font-semibold text-[var(--foreground)]">
          Drop a document here
        </p>

        <p className="mt-2 text-xs leading-5 text-[var(--foreground-muted)]">
          Or click to browse. TXT, Markdown, and PDF files up to 10 MB are
          supported.
        </p>
      </div>

      {selectedFile ? (
        <div className="mt-5">
          <FilePreview
            file={selectedFile}
            disabled={isAnalyzing}
            onRemove={handleRemoveFile}
          />
        </div>
      ) : null}

      <Button
        type="button"
        isLoading={isAnalyzing}
        disabled={!selectedFile || isAnalyzing}
        onClick={handleAnalyze}
        className="mt-5 w-full sm:w-auto"
      >
        Analyze document
      </Button>

      <p className="mt-3 text-xs leading-5 text-[var(--foreground-muted)]">
        The current development environment uses the configured AI provider.
        Analysis results are structured and validated by the backend.
      </p>
    </div>
  );
}