interface AnalysisListSectionProps {
  title: string;
  items: string[];
  emptyMessage: string;
}

export function AnalysisListSection({
  title,
  items,
  emptyMessage,
}: AnalysisListSectionProps) {
  return (
    <section className="rounded-xl border border-[var(--border)] bg-white p-5">
      <div className="flex items-center justify-between gap-4">
        <h3 className="text-sm font-semibold text-[var(--foreground)]">
          {title}
        </h3>

        <span className="rounded-full bg-[var(--surface-subtle)] px-2.5 py-1 text-xs font-semibold text-[var(--foreground-muted)]">
          {items.length}
        </span>
      </div>

      {items.length > 0 ? (
        <ul className="mt-4 space-y-3">
          {items.map((item, index) => (
            <li
              key={`${title}-${index}`}
              className="flex gap-3 text-sm leading-6 text-[var(--foreground-muted)]"
            >
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--primary)]" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-4 text-sm leading-6 text-[var(--foreground-muted)]">
          {emptyMessage}
        </p>
      )}
    </section>
  );
}