import type { DocumentAnalysisResponse } from "@/types/api";

interface AnalysisMetadataProps {
  result: DocumentAnalysisResponse;
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

export function AnalysisMetadata({
  result,
}: AnalysisMetadataProps) {
  const metadataItems = [
    {
      label: "Filename",
      value: result.document.filename,
    },
    {
      label: "File type",
      value: result.document.media_type,
    },
    {
      label: "File size",
      value: formatFileSize(result.document.size_bytes),
    },
    {
      label: "Provider",
      value: result.metadata.provider,
    },
    {
      label: "Model",
      value: result.metadata.model,
    },
    {
      label: "Prompt",
      value: result.metadata.prompt_name,
    },
    {
      label: "Prompt version",
      value: result.metadata.prompt_version,
    },
  ];

  return (
    <section className="rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)] p-5">
      <h3 className="text-sm font-semibold text-[var(--foreground)]">
        Analysis metadata
      </h3>

      <dl className="mt-4 grid gap-4 sm:grid-cols-2">
        {metadataItems.map((item) => (
          <div key={item.label}>
            <dt className="text-xs font-semibold uppercase tracking-[0.1em] text-[var(--foreground-subtle)]">
              {item.label}
            </dt>

            <dd className="mt-1 break-words text-sm font-medium text-[var(--foreground)]">
              {item.value}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}