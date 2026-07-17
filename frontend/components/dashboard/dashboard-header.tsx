interface DashboardHeaderProps {
  isApiConnected: boolean | null;
}

export function DashboardHeader({
  isApiConnected,
}: DashboardHeaderProps) {
  const label =
    isApiConnected === null
      ? "Checking API"
      : isApiConnected
        ? "API connected"
        : "API unavailable";

  return (
    <header className="border-b border-[var(--border)] bg-white">
      <div className="mx-auto flex min-h-18 max-w-7xl items-center justify-between gap-4 px-5 py-4 sm:px-8">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
            Community operations platform
          </p>

          <h1 className="mt-1 truncate text-xl font-semibold tracking-tight text-[var(--foreground)]">
            Document intelligence workspace
          </h1>
        </div>

        <div className="hidden items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--surface-subtle)] px-3 py-2 text-xs font-medium text-[var(--foreground-muted)] sm:flex">
          <span
            aria-hidden="true"
            className={[
              "h-2 w-2 rounded-full",
              isApiConnected === null
                ? "bg-[var(--warning)]"
                : isApiConnected
                  ? "bg-[var(--success)]"
                  : "bg-[var(--danger)]",
            ].join(" ")}
          />
          {label}
        </div>
      </div>
    </header>
  );
}