"use client";

import { useState } from "react";
import { createTask } from "@/lib/api";

type Props = {
  token: string;
  onTaskCreated: () => void;
};

export default function CreateTaskForm({ token, onTaskCreated }: Props) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [projectId, setProjectId] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim() || !projectId) {
      setError("Title and project id are required.");
      return;
    }

    setLoading(true);

    try {
      await createTask(token, {
        title,
        description,
        project_id: Number(projectId),
        assigned_to: assignedTo ? Number(assignedTo) : undefined,
        due_date: dueDate || undefined,
      });

      setTitle("");
      setDescription("");
      setProjectId("");
      setAssignedTo("");
      setDueDate("");
      onTaskCreated();
    } catch {
      setError("Failed to create task");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 rounded bg-white p-4 shadow">
      <h2 className="mb-4 text-xl font-semibold">Create Task</h2>

      <form onSubmit={handleSubmit} className="grid gap-3 md:grid-cols-2">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <input
          type="number"
          placeholder="Project ID"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <input
          type="number"
          placeholder="Assigned User ID"
          value={assignedTo}
          onChange={(e) => setAssignedTo(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="rounded border px-3 py-2 md:col-span-2"
          rows={4}
        />

        {error && <p className="text-sm text-red-600 md:col-span-2">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="rounded bg-green-600 px-4 py-2 text-white md:col-span-2 disabled:opacity-60"
        >
          {loading ? "Creating..." : "Create Task"}
        </button>
      </form>
    </div>
  );
}