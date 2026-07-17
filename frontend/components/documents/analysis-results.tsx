import { AnalysisListSection } from "@/components/documents/analysis-list-section";
import { AnalysisMetadata } from "@/components/documents/analysis-metadata";
import type { DocumentAnalysisResponse } from "@/types/api";

interface AnalysisResultsProps {
  result: DocumentAnalysisResponse;
}

function formatObjectItem(item: Record<string, unknown>): string {
  const preferredFields = [
    "description",
    "action",
    "requirement",
    "deadline",
    "document",
    "risk",
    "recommendation",
    "title",
    "name",
    "text",
  ];

  for (const field of preferredFields) {
    const value = item[field];

    if (typeof value === "string" && value.trim()) {
      return value;
    }
  }

  const readableValues = Object.values(item).filter(
    (value): value is string =>
      typeof value === "string" && value.trim().length > 0,
  );

  if (readableValues.length > 0) {
    return readableValues.join(" — ");
  }

  return JSON.stringify(item);
}

function formatAnalysisItems(items: readonly unknown[]): string[] {
  return items.map((item) => {
    if (typeof item === "string") {
      return item;
    }

    if (typeof item === "number" || typeof item === "boolean") {
      return String(item);
    }

    if (item && typeof item === "object" && !Array.isArray(item)) {
      return formatObjectItem(item as Record<string, unknown>);
    }

    return String(item);
  });
}

export function AnalysisResults({ result }: AnalysisResultsProps) {
  const { analysis } = result;

  return (
    <div className="mt-6 space-y-6">
      <section className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-[var(--shadow-sm)]">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--success)]">
              Analysis complete
            </p>

            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-[var(--foreground)]">
              Structured operational findings
            </h2>

            <p className="mt-2 text-sm text-[var(--foreground-muted)]">
              Reviewed document: {result.document.filename}
            </p>
          </div>

          <div className="w-fit rounded-full bg-[var(--success-subtle)] px-3 py-1.5 text-xs font-semibold text-[var(--success)]">
            Validated response
          </div>
        </div>

        <div className="mt-6 rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)] p-5">
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--primary)]">
            Executive summary
          </p>

          <p className="mt-3 text-sm leading-7 text-[var(--foreground)]">
            {analysis.executive_summary}
          </p>
        </div>
      </section>

      <div className="grid gap-4 lg:grid-cols-2">
        <AnalysisListSection
          title="Key action items"
          items={formatAnalysisItems(analysis.key_action_items)}
          emptyMessage="No key action items were identified."
        />

        <AnalysisListSection
          title="Eligibility requirements"
          items={formatAnalysisItems(analysis.eligibility_requirements)}
          emptyMessage="No eligibility requirements were identified."
        />

        <AnalysisListSection
          title="Important deadlines"
          items={formatAnalysisItems(analysis.important_deadlines)}
          emptyMessage="No deadlines were identified."
        />

        <AnalysisListSection
          title="Required documents"
          items={formatAnalysisItems(analysis.required_documents)}
          emptyMessage="No required documents were identified."
        />

        <AnalysisListSection
          title="Risks and concerns"
          items={formatAnalysisItems(analysis.risks)}
          emptyMessage="No risks or concerns were identified."
        />

        <AnalysisListSection
          title="Recommended next steps"
          items={formatAnalysisItems(analysis.recommended_next_steps)}
          emptyMessage="No next steps were recommended."
        />
      </div>

      <AnalysisMetadata result={result} />
    </div>
  );
}