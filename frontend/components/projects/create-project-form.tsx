"use client";

import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import type { ProjectCreate } from "@/types/api";

interface CreateProjectFormProps {
  onSubmit: (payload: ProjectCreate) => Promise<void>;
  isSubmitting?: boolean;
}

export function CreateProjectForm({
  onSubmit,
  isSubmitting = false,
}: CreateProjectFormProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedName = name.trim();
    const cleanedDescription = description.trim();

    if (!cleanedName) {
      return;
    }

    await onSubmit({
      name: cleanedName,
      description: cleanedDescription || null,
    });

    setName("");
    setDescription("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-[var(--border)] bg-[var(--surface-subtle)] p-4"
    >
      <div>
        <label
          htmlFor="project-name"
          className="text-sm font-semibold text-[var(--foreground)]"
        >
          Project name
        </label>

        <input
          id="project-name"
          name="project-name"
          type="text"
          value={name}
          disabled={isSubmitting}
          onChange={(event) => setName(event.target.value)}
          placeholder="Housing support policy review"
          className="mt-2 w-full rounded-lg border border-[var(--border-strong)] bg-white px-3 py-2.5 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary-subtle)] disabled:cursor-not-allowed disabled:opacity-60"
        />
      </div>

      <div className="mt-4">
        <label
          htmlFor="project-description"
          className="text-sm font-semibold text-[var(--foreground)]"
        >
          Description
        </label>

        <textarea
          id="project-description"
          name="project-description"
          value={description}
          disabled={isSubmitting}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Review eligibility requirements, required documents, deadlines, and escalation procedures."
          rows={4}
          className="mt-2 w-full resize-y rounded-lg border border-[var(--border-strong)] bg-white px-3 py-2.5 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary-subtle)] disabled:cursor-not-allowed disabled:opacity-60"
        />
      </div>

      <Button
        type="submit"
        isLoading={isSubmitting}
        disabled={!name.trim() || isSubmitting}
        className="mt-4 w-full sm:w-auto"
      >
        Create project
      </Button>
    </form>
  );
}