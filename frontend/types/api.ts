export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  pages: number;
}

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceCreate {
  name: string;
  slug: string;
}

export interface WorkspaceUpdate {
  name?: string;
  slug?: string;
}

export type WorkspaceListResponse = PaginatedResponse<Workspace>;

export interface Project {
  id: string;
  workspace_id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string | null;
}

export interface ProjectUpdate {
  name?: string;
  description?: string | null;
}

export type ProjectListResponse = PaginatedResponse<Project>;

export type Priority = "low" | "medium" | "high";

export interface ActionItem {
  action: string;
  priority: Priority;
  owner: string | null;
  deadline: string | null;
}

export interface EligibilityRequirement {
  requirement: string;
  evidence: string | null;
}

export interface ImportantDeadline {
  description: string;
  date: string | null;
  source_text: string | null;
}

export interface AnalysisRisk {
  description: string;
  severity: Priority;
  mitigation: string | null;
}

export interface DocumentAnalysis {
  executive_summary: string;
  key_action_items: ActionItem[];
  eligibility_requirements: EligibilityRequirement[];
  important_deadlines: ImportantDeadline[];
  required_documents: string[];
  risks: AnalysisRisk[];
  recommended_next_steps: string[];
}

export interface DocumentMetadata {
  filename: string;
  media_type: string;
  size_bytes: number;
}

export interface AnalysisMetadata {
  prompt_name: string;
  prompt_version: string;
  provider: string;
  model: string;
}

export interface DocumentAnalysisResponse {
  document: DocumentMetadata;
  analysis: DocumentAnalysis;
  metadata: AnalysisMetadata;
}

export interface ApiErrorDetail {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
}

export interface ApiErrorResponse {
  detail?: string | ApiErrorDetail[];
  message?: string;
  error?: string;
}