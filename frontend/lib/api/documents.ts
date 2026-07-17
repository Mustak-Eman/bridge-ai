import { apiRequest } from "@/lib/api/client";
import type { DocumentAnalysisResponse } from "@/types/api";

export async function analyzeDocument(
  file: File,
): Promise<DocumentAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<DocumentAnalysisResponse>("/documents/analyze", {
    method: "POST",
    body: formData,
  });
}