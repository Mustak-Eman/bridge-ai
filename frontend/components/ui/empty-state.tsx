import type { ReactNode } from "react";

interface EmptyStateProps {
  eyebrow?: string;
  title: string;
  description: string;
  action?: ReactNode;
}

export function EmptyState({
  eyebrow,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex min-h-64 flex-col items-center justify-center rounded-2xl border border-dashed border-[var(--border-strong)] bg-[var(--surface-subtle)] px-6 py-12 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[var(--primary-subtle)] text-lg font-bold text-[var(--primary)]">
        AI
      </div>

      {eyebrow ? (
        <p className="mt-5 text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
          {eyebrow}
        </p>
      ) : null}

      <h2 className="mt-2 text-lg font-semibold text-[var(--foreground)]">
        {title}
      </h2>

      <p className="mt-2 max-w-md text-sm leading-6 text-[var(--foreground-muted)]">
        {description}
      </p>

      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  );
}