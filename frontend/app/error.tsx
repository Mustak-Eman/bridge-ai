"use client";

import { Button } from "@/components/ui/button";
import { ErrorAlert } from "@/components/ui/error-alert";

interface GlobalErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--background)] px-5">
      <div className="w-full max-w-xl rounded-2xl border border-[var(--border)] bg-white p-6 shadow-[var(--shadow-md)]">
        <ErrorAlert
          title="Bridge AI could not load"
          message={
            error.message ||
            "An unexpected frontend error prevented the application from loading."
          }
        />

        <Button className="mt-5" onClick={reset}>
          Try again
        </Button>
      </div>
    </div>
  );
}