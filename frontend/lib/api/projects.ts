import { apiRequest } from "@/lib/api/client";
import type {
  Project,
  ProjectCreate,
  ProjectListResponse,
  ProjectUpdate,
} from "@/types/api";

interface ListProjectsOptions {
  page?: number;
  pageSize?: number;
}

export async function listProjects(
  workspaceId: string,
  options: ListProjectsOptions = {},
): Promise<ProjectListResponse> {
  const page = options.page ?? 1;
  const pageSize = options.pageSize ?? 100;

  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });

  return apiRequest<ProjectListResponse>(
    `/workspaces/${workspaceId}/projects?${params.toString()}`,
  );
}

export async function getProject(projectId: string): Promise<Project> {
  return apiRequest<Project>(`/projects/${projectId}`);
}

export async function createProject(
  workspaceId: string,
  payload: ProjectCreate,
): Promise<Project> {
  return apiRequest<Project>(`/workspaces/${workspaceId}/projects`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function updateProject(
  projectId: string,
  payload: ProjectUpdate,
): Promise<Project> {
  return apiRequest<Project>(`/projects/${projectId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function deleteProject(projectId: string): Promise<void> {
  return apiRequest<void>(`/projects/${projectId}`, {
    method: "DELETE",
  });
}