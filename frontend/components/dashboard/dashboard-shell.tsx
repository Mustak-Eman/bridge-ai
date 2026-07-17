import type { ReactNode } from "react";

import { DashboardHeader } from "@/components/dashboard/dashboard-header";
import { Sidebar } from "@/components/dashboard/sidebar";
import { WorkflowProgress } from "@/components/dashboard/workflow-progress";

interface DashboardShellProps {
  children: ReactNode;
  isApiConnected: boolean | null;
}

export function DashboardShell({
  children,
  isApiConnected,
}: DashboardShellProps) {
  return (
    <div className="min-h-screen bg-[var(--background)] lg:flex">
      <Sidebar />

      <div className="min-w-0 flex-1">
        <DashboardHeader isApiConnected={isApiConnected} />

        <main className="mx-auto max-w-7xl px-5 py-6 sm:px-8 sm:py-8">
          <div className="mb-6 lg:hidden">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[var(--sidebar)] text-sm font-bold text-white">
                BA
              </div>

              <div>
                <p className="font-semibold text-[var(--foreground)]">
                  Bridge AI
                </p>
                <p className="text-xs text-[var(--foreground-muted)]">
                  Operations intelligence
                </p>
              </div>
            </div>
          </div>

          <WorkflowProgress />

          <div className="mt-6">{children}</div>
        </main>
      </div>
    </div>
  );
}