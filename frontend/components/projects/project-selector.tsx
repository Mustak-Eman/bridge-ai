import type { Project } from "@/types/api";

interface ProjectSelectorProps {
  projects: Project[];
  selectedProjectId: string;
  disabled?: boolean;
  onChange: (projectId: string) => void;
}

export function ProjectSelector({
  projects,
  selectedProjectId,
  disabled = false,
  onChange,
}: ProjectSelectorProps) {
  return (
    <div>
      <label
        htmlFor="project-selector"
        className="text-sm font-semibold text-[var(--foreground)]"
      >
        Active project
      </label>

      <select
        id="project-selector"
        value={selectedProjectId}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
        className={[
          "mt-2 min-h-11 w-full rounded-lg border border-[var(--border-strong)]",
          "bg-white px-3 text-sm text-[var(--foreground)]",
          "transition-colors hover:border-[#98a2b3]",
          "disabled:cursor-not-allowed disabled:bg-[var(--surface-strong)]",
          "disabled:text-[var(--foreground-subtle)]",
        ].join(" ")}
      >
        <option value="">Select a project</option>

        {projects.map((project) => (
          <option key={project.id} value={project.id}>
            {project.name}
          </option>
        ))}
      </select>

      <p className="mt-2 text-xs leading-5 text-[var(--foreground-muted)]">
        Document analysis will be associated with this operational initiative.
      </p>
    </div>
  );
}