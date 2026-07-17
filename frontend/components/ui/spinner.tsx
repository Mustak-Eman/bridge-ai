interface SpinnerProps {
  label?: string;
}

export function Spinner({ label = "Loading" }: SpinnerProps) {
  return (
    <div
      className="inline-flex items-center gap-2 text-sm text-[var(--foreground-muted)]"
      role="status"
    >
      <span
        aria-hidden="true"
        className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--border-strong)] border-r-[var(--primary)]"
      />
      <span>{label}</span>
    </div>
  );
}