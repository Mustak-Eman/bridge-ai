const workflowItems = [
  {
    number: "01",
    label: "Workspace",
    description: "Choose your organization",
  },
  {
    number: "02",
    label: "Project",
    description: "Select an operational initiative",
  },
  {
    number: "03",
    label: "Document",
    description: "Upload source material",
  },
  {
    number: "04",
    label: "Analysis",
    description: "Review structured findings",
  },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 shrink-0 bg-[var(--sidebar)] px-5 py-6 text-white lg:flex lg:flex-col">
      <div className="flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-sm font-bold text-[var(--sidebar)]">
          BA
        </div>

        <div>
          <p className="font-semibold tracking-tight">Bridge AI</p>
          <p className="text-xs text-[var(--sidebar-muted)]">
            Operations intelligence
          </p>
        </div>
      </div>

      <nav className="mt-10" aria-label="Application workflow">
        <p className="px-2 text-xs font-semibold uppercase tracking-[0.14em] text-[var(--sidebar-muted)]">
          Analysis workflow
        </p>

        <ol className="mt-4 space-y-2">
          {workflowItems.map((item, index) => (
            <li
              key={item.number}
              className={[
                "rounded-xl px-3 py-3",
                index === 0
                  ? "bg-[var(--sidebar-active)]"
                  : "text-[var(--sidebar-muted)]",
              ].join(" ")}
            >
              <div className="flex gap-3">
                <span
                  className={[
                    "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-xs font-bold",
                    index === 0
                      ? "bg-white text-[var(--sidebar)]"
                      : "border border-white/10",
                  ].join(" ")}
                >
                  {item.number}
                </span>

                <div>
                  <p
                    className={[
                      "text-sm font-semibold",
                      index === 0 ? "text-white" : "",
                    ].join(" ")}
                  >
                    {item.label}
                  </p>
                  <p className="mt-0.5 text-xs leading-5">
                    {item.description}
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ol>
      </nav>

      <div className="mt-auto rounded-xl border border-white/10 bg-white/5 p-4">
        <div className="flex items-center gap-2">
          <span
            aria-hidden="true"
            className="h-2 w-2 rounded-full bg-[#47cd89]"
          />
          <p className="text-sm font-medium">System ready</p>
        </div>

        <p className="mt-2 text-xs leading-5 text-[var(--sidebar-muted)]">
          Structured document analysis is available through the configured AI
          provider.
        </p>
      </div>
    </aside>
  );
}