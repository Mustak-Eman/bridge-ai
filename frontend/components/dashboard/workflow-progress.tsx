const steps = [
  "Create workspace",
  "Create project",
  "Upload document",
  "Review analysis",
];

export function WorkflowProgress() {
  return (
    <section
      aria-labelledby="workflow-heading"
      className="rounded-2xl border border-[var(--border)] bg-white p-5 shadow-[var(--shadow-sm)]"
    >
      <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--primary)]">
            Guided workflow
          </p>
          <h2
            id="workflow-heading"
            className="mt-1 text-base font-semibold text-[var(--foreground)]"
          >
            Turn operational documents into actionable information
          </h2>
        </div>

        <p className="text-sm text-[var(--foreground-muted)]">
          Step 1 of 4
        </p>
      </div>

      <ol className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {steps.map((step, index) => (
          <li
            key={step}
            className={[
              "rounded-xl border px-4 py-3",
              index === 0
                ? "border-[#c7d2fe] bg-[var(--primary-subtle)]"
                : "border-[var(--border)] bg-[var(--surface-subtle)]",
            ].join(" ")}
          >
            <div className="flex items-center gap-3">
              <span
                className={[
                  "flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold",
                  index === 0
                    ? "bg-[var(--primary)] text-white"
                    : "bg-white text-[var(--foreground-muted)]",
                ].join(" ")}
              >
                {index + 1}
              </span>

              <span
                className={[
                  "text-sm font-medium",
                  index === 0
                    ? "text-[var(--primary)]"
                    : "text-[var(--foreground-muted)]",
                ].join(" ")}
              >
                {step}
              </span>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}