"use client";

import { useEffect, useState } from "react";

import { ErrorAlert } from "@/components/ui/error-alert";
import { Spinner } from "@/components/ui/spinner";
import { CreateWorkspaceForm } from "@/components/workspaces/create-workspace-form";
import { WorkspaceSelector } from "@/components/workspaces/workspace-selector";
import { createWorkspace, listWorkspaces } from "@/lib/api/workspaces";
import { getErrorMessage } from "@/lib/get-error-message";
import type { Workspace, WorkspaceCreate } from "@/types/api";

interface WorkspacePanelProps {
  selectedWorkspaceId: string;
  onWorkspaceChange: (workspaceId: string) => void;
  onConnectionChange: (isConnected: boolean) => void;
}

export function WorkspacePanel({
  selectedWorkspaceId,
  onWorkspaceChange,
  onConnectionChange,
}: WorkspacePanelProps) {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let isCancelled = false;

    async function fetchWorkspaces() {
      try {
        const response = await listWorkspaces();

        if (isCancelled) {
          return;
        }

        setWorkspaces(response.items);
        onConnectionChange(true);
      } catch (error) {
        if (isCancelled) {
          return;
        }

        setErrorMessage(getErrorMessage(error));
        onConnectionChange(false);
      } finally {
        if (!isCancelled) {
          setIsLoading(false);
        }
      }
    }

    void fetchWorkspaces();

    return () => {
      isCancelled = true;
    };
  }, [onConnectionChange]);

  async function handleCreateWorkspace(payload: WorkspaceCreate) {
    setIsCreating(true);
    setErrorMessage(null);

    try {
      const workspace = await createWorkspace(payload);

      setWorkspaces((currentWorkspaces) => [
        ...currentWorkspaces,
        workspace,
      ]);

      onWorkspaceChange(workspace.id);
      onConnectionChange(true);
    } catch (error) {
      setErrorMessage(getErrorMessage(error));
      onConnectionChange(false);
      throw error;
    } finally {
      setIsCreating(false);
    }
  }

  return (
    <div>
      {errorMessage ? (
        <ErrorAlert
          title="Workspace request failed"
          message={errorMessage}
          onDismiss={() => setErrorMessage(null)}
        />
      ) : null}

      <div className={errorMessage ? "mt-5" : ""}>
        {isLoading ? (
          <div className="flex min-h-28 items-center justify-center rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)]">
            <Spinner label="Loading workspaces" />
          </div>
        ) : (
          <WorkspaceSelector
            workspaces={workspaces}
            selectedWorkspaceId={selectedWorkspaceId}
            onChange={onWorkspaceChange}
          />
        )}
      </div>

      <div className="my-5 h-px bg-[var(--border)]" />

      <CreateWorkspaceForm
        isSubmitting={isCreating}
        onSubmit={handleCreateWorkspace}
      />

      {!isLoading && workspaces.length === 0 ? (
        <p className="mt-4 rounded-lg bg-[var(--warning-subtle)] px-3 py-2 text-xs leading-5 text-[var(--warning)]">
          No workspaces exist yet. Create the first workspace to continue.
        </p>
      ) : null}
    </div>
  );
}