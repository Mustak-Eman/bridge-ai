interface ErrorAlertProps {
  title?: string;
  message: string;
  onDismiss?: () => void;
}

export function ErrorAlert({
  title = "Something went wrong",
  message,
  onDismiss,
}: ErrorAlertProps) {
  return (
    <div
      className="flex items-start justify-between gap-4 rounded-xl border border-[#fecdca] bg-[var(--danger-subtle)] p-4"
      role="alert"
    >
      <div>
        <p className="text-sm font-semibold text-[var(--danger)]">{title}</p>
        <p className="mt-1 text-sm leading-6 text-[#912018]">{message}</p>
      </div>

      {onDismiss ? (
        <button
          type="button"
          onClick={onDismiss}
          className="rounded-md px-2 py-1 text-sm font-medium text-[var(--danger)] hover:bg-white/70"
          aria-label="Dismiss error"
        >
          Close
        </button>
      ) : null}
    </div>
  );
}