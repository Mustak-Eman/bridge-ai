interface FilePreviewProps {
  file: File;
  onRemove: () => void;
  disabled?: boolean;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} bytes`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function FilePreview({
  file,
  onRemove,
  disabled = false,
}: FilePreviewProps) {
  return (
    <div className="flex items-start justify-between gap-4 rounded-xl border border-[var(--border)] bg-white p-4">
      <div className="min-w-0">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--primary-subtle)] text-xs font-bold uppercase text-[var(--primary)]">
            {file.name.split(".").pop()?.slice(0, 4) ?? "FILE"}
          </div>

          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-[var(--foreground)]">
              {file.name}
            </p>

            <p className="mt-1 text-xs text-[var(--foreground-muted)]">
              {formatFileSize(file.size)}
            </p>
          </div>
        </div>
      </div>

      <button
        type="button"
        disabled={disabled}
        onClick={onRemove}
        className="shrink-0 rounded-lg px-3 py-2 text-xs font-semibold text-[var(--danger)] transition-colors hover:bg-[var(--danger-subtle)] disabled:cursor-not-allowed disabled:opacity-50"
      >
        Remove
      </button>
    </div>
  );
}