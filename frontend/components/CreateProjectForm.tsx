"use client";

import { useState } from "react";
import { createProject } from "@/lib/api";

type Props = {
  token: string;
  onProjectCreated: () => void;
};

export default function CreateProjectForm({ token, onProjectCreated }: Props) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }

    setLoading(true);

    try {
      await createProject(token, {
        name,
        description,
      });

      setName("");
      setDescription("");
      onProjectCreated();
    } catch {
      setError("Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 rounded bg-white p-4 shadow">
      <h2 className="mb-4 text-xl font-semibold">Create Project</h2>

      <form onSubmit={handleSubmit} className="grid gap-3">
        <input
          type="text"
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <textarea
          placeholder="Project description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="rounded border px-3 py-2"
          rows={4}
        />

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="rounded bg-green-600 px-4 py-2 text-white disabled:opacity-60"
        >
          {loading ? "Creating..." : "Create Project"}
        </button>
      </form>
    </div>
  );
}