import { apiRequest } from "@/lib/api/client";
import type {
  Workspace,
  WorkspaceCreate,
  WorkspaceListResponse,
  WorkspaceUpdate,
} from "@/types/api";

interface ListWorkspacesOptions {
  page?: number;
  pageSize?: number;
}

export async function listWorkspaces(
  options: ListWorkspacesOptions = {},
): Promise<WorkspaceListResponse> {
  const page = options.page ?? 1;
  const pageSize = options.pageSize ?? 100;

  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });

  return apiRequest<WorkspaceListResponse>(
    `/workspaces?${params.toString()}`,
  );
}

export async function getWorkspace(
  workspaceId: string,
): Promise<Workspace> {
  return apiRequest<Workspace>(`/workspaces/${workspaceId}`);
}

export async function createWorkspace(
  payload: WorkspaceCreate,
): Promise<Workspace> {
  return apiRequest<Workspace>("/workspaces", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function updateWorkspace(
  workspaceId: string,
  payload: WorkspaceUpdate,
): Promise<Workspace> {
  return apiRequest<Workspace>(`/workspaces/${workspaceId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function deleteWorkspace(
  workspaceId: string,
): Promise<void> {
  return apiRequest<void>(`/workspaces/${workspaceId}`, {
    method: "DELETE",
  });
}