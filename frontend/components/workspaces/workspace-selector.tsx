import type { Workspace } from "@/types/api";

interface WorkspaceSelectorProps {
  workspaces: Workspace[];
  selectedWorkspaceId: string;
  disabled?: boolean;
  onChange: (workspaceId: string) => void;
}

export function WorkspaceSelector({
  workspaces,
  selectedWorkspaceId,
  disabled = false,
  onChange,
}: WorkspaceSelectorProps) {
  return (
    <div>
      <label
        htmlFor="workspace-selector"
        className="text-sm font-semibold text-[var(--foreground)]"
      >
        Active workspace
      </label>

      <select
        id="workspace-selector"
        value={selectedWorkspaceId}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
        className={[
          "mt-2 min-h-11 w-full rounded-lg border border-[var(--border-strong)]",
          "bg-white px-3 text-sm text-[var(--foreground)]",
          "transition-colors hover:border-[#98a2b3]",
          "disabled:bg-[var(--surface-strong)] disabled:text-[var(--foreground-subtle)]",
        ].join(" ")}
      >
        <option value="">Select a workspace</option>

        {workspaces.map((workspace) => (
          <option key={workspace.id} value={workspace.id}>
            {workspace.name}
          </option>
        ))}
      </select>

      <p className="mt-2 text-xs leading-5 text-[var(--foreground-muted)]">
        Projects and document analysis will be scoped to this workspace.
      </p>
    </div>
  );
}