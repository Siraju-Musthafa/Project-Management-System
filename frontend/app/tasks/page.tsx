"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import CreateTaskForm from "@/components/CreateTaskForm";
import Pagination from "@/components/Pagination";
import { getTasks, Task, updateTaskStatus } from "@/lib/api";

const statusOptions = ["todo", "in_progress", "done", "blocked"];

export default function TasksPage() {
  const router = useRouter();
  const [token, setToken] = useState("");
  const [role, setRole] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [size] = useState(5);
  const [totalPages, setTotalPages] = useState(1);
  const [updatingTaskId, setUpdatingTaskId] = useState<number | null>(null);

  const loadTasks = useCallback(
    async (authToken: string, currentPage: number) => {
      try {
        setError("");
        const data = await getTasks(authToken, currentPage, size);
        setTasks(data.items);
        setTotalPages(Math.max(1, Math.ceil(data.total / data.size)));
      } catch {
        setError("Failed to load tasks");
      }
    },
    [size]
  );

  useEffect(() => {
    const savedToken = localStorage.getItem("access_token");
    const savedRole = localStorage.getItem("user_role") || "";

    if (!savedToken) {
      router.push("/login");
      return;
    }

    setToken(savedToken);
    setRole(savedRole);
    loadTasks(savedToken, page);
  }, [router, loadTasks, page]);

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    if (!token) return;

    setUpdatingTaskId(taskId);
    setError("");

    try {
      const updatedTask = await updateTaskStatus(token, taskId, newStatus);

      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? { ...task, status: updatedTask.status } : task
        )
      );
    } catch {
      setError("Failed to update task status");
    } finally {
      setUpdatingTaskId(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="p-6">
        <h1 className="mb-4 text-2xl font-bold">Tasks</h1>

        {role === "admin" && token && (
          <CreateTaskForm token={token} onTaskCreated={() => loadTasks(token, page)} />
        )}

        {error && <p className="mb-4 text-red-600">{error}</p>}

        <div className="grid gap-4">
          {tasks.map((task) => (
            <div key={task.id} className="rounded bg-white p-4 shadow">
              <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div>
                  <h2 className="text-lg font-semibold">{task.title}</h2>
                  <p className="mt-2 text-gray-600">
                    {task.description || "No description"}
                  </p>

                  <div className="mt-3 space-y-1 text-sm text-gray-700">
                    <p>Project ID: {task.project_id}</p>
                    <p>Assigned To: {task.assigned_to ?? "Not assigned"}</p>
                    <p>Due Date: {task.due_date || "No due date"}</p>
                  </div>
                </div>

                <div className="min-w-[220px]">
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    Task Status
                  </label>

                  <select
                    value={task.status}
                    onChange={(e) => handleStatusChange(task.id, e.target.value)}
                    disabled={updatingTaskId === task.id}
                    className="w-full rounded border px-3 py-2"
                  >
                    {statusOptions.map((status) => (
                      <option key={status} value={status}>
                        {status}
                      </option>
                    ))}
                  </select>

                  {updatingTaskId === task.id && (
                    <p className="mt-2 text-sm text-blue-600">Updating status...</p>
                  )}
                </div>
              </div>
            </div>
          ))}

          {tasks.length === 0 && !error && (
            <p className="text-gray-600">No tasks found.</p>
          )}
        </div>

        <Pagination
          currentPage={page}
          totalPages={totalPages}
          onPageChange={setPage}
        />
      </div>
    </div>
  );
}