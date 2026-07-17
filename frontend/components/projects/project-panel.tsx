"use client";

import { useEffect, useState } from "react";

import { CreateProjectForm } from "@/components/projects/create-project-form";
import { ProjectSelector } from "@/components/projects/project-selector";
import { ErrorAlert } from "@/components/ui/error-alert";
import { Spinner } from "@/components/ui/spinner";
import { createProject, listProjects } from "@/lib/api/projects";
import { getErrorMessage } from "@/lib/get-error-message";
import type { Project, ProjectCreate } from "@/types/api";

interface ProjectPanelProps {
  workspaceId: string;
  selectedProjectId: string;
  onProjectChange: (projectId: string) => void;
  onConnectionChange: (isConnected: boolean) => void;
}

export function ProjectPanel({
  workspaceId,
  selectedProjectId,
  onProjectChange,
  onConnectionChange,
}: ProjectPanelProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let isCancelled = false;

    async function fetchProjects() {
      try {
        const response = await listProjects(workspaceId);

        if (isCancelled) {
          return;
        }

        setProjects(response.items);
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

    void fetchProjects();

    return () => {
      isCancelled = true;
    };
  }, [workspaceId, onConnectionChange]);

  async function handleCreateProject(payload: ProjectCreate) {
    setIsCreating(true);
    setErrorMessage(null);

    try {
      const project = await createProject(workspaceId, payload);

      setProjects((currentProjects) => [...currentProjects, project]);
      onProjectChange(project.id);
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
          title="Project request failed"
          message={errorMessage}
          onDismiss={() => setErrorMessage(null)}
        />
      ) : null}

      <div className={errorMessage ? "mt-5" : ""}>
        {isLoading ? (
          <div className="flex min-h-28 items-center justify-center rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)]">
            <Spinner label="Loading projects" />
          </div>
        ) : (
          <ProjectSelector
            projects={projects}
            selectedProjectId={selectedProjectId}
            onChange={onProjectChange}
          />
        )}
      </div>

      <div className="my-5 h-px bg-[var(--border)]" />

      <CreateProjectForm
        isSubmitting={isCreating}
        onSubmit={handleCreateProject}
      />

      {!isLoading && projects.length === 0 ? (
        <p className="mt-4 rounded-lg bg-[var(--warning-subtle)] px-3 py-2 text-xs leading-5 text-[var(--warning)]">
          This workspace has no projects yet. Create one to continue.
        </p>
      ) : null}
    </div>
  );
}