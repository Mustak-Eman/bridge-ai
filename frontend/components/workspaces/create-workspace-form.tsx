"use client";

import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import type { WorkspaceCreate } from "@/types/api";

interface CreateWorkspaceFormProps {
  isSubmitting: boolean;
  onSubmit: (payload: WorkspaceCreate) => Promise<void>;
}

function createSlug(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

export function CreateWorkspaceForm({
  isSubmitting,
  onSubmit,
}: CreateWorkspaceFormProps) {
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [slugWasEdited, setSlugWasEdited] = useState(false);

  function handleNameChange(value: string) {
    setName(value);

    if (!slugWasEdited) {
      setSlug(createSlug(value));
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedName = name.trim();
    const cleanedSlug = slug.trim();

    if (!cleanedName || !cleanedSlug) {
      return;
    }

    await onSubmit({
      name: cleanedName,
      slug: cleanedSlug,
    });

    setName("");
    setSlug("");
    setSlugWasEdited(false);
  }

  const isValid = name.trim().length > 0 && slug.trim().length > 0;

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)] p-4"
    >
      <div>
        <h3 className="text-sm font-semibold text-[var(--foreground)]">
          Create a workspace
        </h3>
        <p className="mt-1 text-xs leading-5 text-[var(--foreground-muted)]">
          A workspace represents the organization or operating unit using
          Bridge AI.
        </p>
      </div>

      <div className="mt-4 grid gap-4">
        <div>
          <label
            htmlFor="workspace-name"
            className="text-sm font-medium text-[var(--foreground)]"
          >
            Workspace name
          </label>

          <input
            id="workspace-name"
            name="workspace-name"
            type="text"
            required
            maxLength={150}
            value={name}
            disabled={isSubmitting}
            placeholder="Bronx Community Services"
            onChange={(event) => handleNameChange(event.target.value)}
            className={[
              "mt-2 min-h-11 w-full rounded-lg border border-[var(--border-strong)]",
              "bg-white px-3 text-sm text-[var(--foreground)]",
              "placeholder:text-[var(--foreground-subtle)]",
              "disabled:bg-[var(--surface-strong)]",
            ].join(" ")}
          />
        </div>

        <div>
          <label
            htmlFor="workspace-slug"
            className="text-sm font-medium text-[var(--foreground)]"
          >
            Workspace slug
          </label>

          <input
            id="workspace-slug"
            name="workspace-slug"
            type="text"
            required
            maxLength={100}
            pattern="[a-z0-9]+(?:-[a-z0-9]+)*"
            value={slug}
            disabled={isSubmitting}
            placeholder="bronx-community-services"
            onChange={(event) => {
              setSlug(event.target.value.toLowerCase());
              setSlugWasEdited(true);
            }}
            className={[
              "mt-2 min-h-11 w-full rounded-lg border border-[var(--border-strong)]",
              "bg-white px-3 font-mono text-sm text-[var(--foreground)]",
              "placeholder:text-[var(--foreground-subtle)]",
              "disabled:bg-[var(--surface-strong)]",
            ].join(" ")}
          />

          <p className="mt-1 text-xs text-[var(--foreground-muted)]">
            Use lowercase letters, numbers, and hyphens only.
          </p>
        </div>
      </div>

      <Button
        type="submit"
        isLoading={isSubmitting}
        disabled={!isValid}
        className="mt-4 w-full sm:w-auto"
      >
        Create workspace
      </Button>
    </form>
  );
}