"use client";

import { useState } from "react";

import { DashboardShell } from "@/components/dashboard/dashboard-shell";
import { AnalysisResults } from "@/components/documents/analysis-results";
import { DocumentUploadPanel } from "@/components/documents/document-upload-panel";
import { ProjectPanel } from "@/components/projects/project-panel";
import { EmptyState } from "@/components/ui/empty-state";
import { WorkspacePanel } from "@/components/workspaces/workspace-panel";
import type { DocumentAnalysisResponse } from "@/types/api";

export function DashboardController() {
  const [selectedWorkspaceId, setSelectedWorkspaceId] = useState("");
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [isApiConnected, setIsApiConnected] = useState<boolean | null>(null);
  const [analysisResult, setAnalysisResult] =
    useState<DocumentAnalysisResponse | null>(null);

  function handleWorkspaceChange(workspaceId: string) {
    setSelectedWorkspaceId(workspaceId);
    setSelectedProjectId("");
    setAnalysisResult(null);
  }

  function handleProjectChange(projectId: string) {
    setSelectedProjectId(projectId);
    setAnalysisResult(null);
  }

  function handleAnalysisComplete(result: DocumentAnalysisResponse) {
    setAnalysisResult(result);
  }

  return (
    <DashboardShell isApiConnected={isApiConnected}>
      <section className="grid gap-6 xl:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
        <div className="space-y-6">
          <div className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-[var(--shadow-sm)]">
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
              Workspace setup
            </p>

            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-[var(--foreground)]">
              Organize analysis around real operational work
            </h2>

            <p className="mt-3 max-w-xl text-sm leading-6 text-[var(--foreground-muted)]">
              Create or select the organization responsible for the program,
              service, policy, or operational process being analyzed.
            </p>

            <div className="mt-6">
              <WorkspacePanel
                selectedWorkspaceId={selectedWorkspaceId}
                onWorkspaceChange={handleWorkspaceChange}
                onConnectionChange={setIsApiConnected}
              />
            </div>
          </div>

          {selectedWorkspaceId ? (
            <div className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-[var(--shadow-sm)]">
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
                Project setup
              </p>

              <h2 className="mt-2 text-xl font-semibold tracking-tight text-[var(--foreground)]">
                Select the operational initiative
              </h2>

              <p className="mt-3 text-sm leading-6 text-[var(--foreground-muted)]">
                Projects keep document analysis scoped to a specific program,
                service area, policy review, or operational objective.
              </p>

              <div className="mt-6">
                <ProjectPanel
                  workspaceId={selectedWorkspaceId}
                  selectedProjectId={selectedProjectId}
                  onProjectChange={handleProjectChange}
                  onConnectionChange={setIsApiConnected}
                />
              </div>
            </div>
          ) : null}
        </div>

        <div>
          {selectedProjectId ? (
            <DocumentUploadPanel
              projectId={selectedProjectId}
              onAnalysisComplete={handleAnalysisComplete}
              onConnectionChange={setIsApiConnected}
            />
          ) : (
            <EmptyState
              eyebrow="Analysis area"
              title={
                selectedWorkspaceId
                  ? "Create or select a project"
                  : "Start by creating a workspace"
              }
              description={
                selectedWorkspaceId
                  ? "Choose an existing project or create a new operational initiative before uploading documents."
                  : "Once a workspace and project are selected, this area will accept TXT, Markdown, and PDF documents and display structured AI findings."
              }
            />
          )}

          {analysisResult ? (
            <AnalysisResults result={analysisResult} />
          ) : null}
        </div>
      </section>
    </DashboardShell>
  );
}