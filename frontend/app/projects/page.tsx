"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import useSWR from "swr";
import Navbar from "@/components/Navbar";
import CreateProjectForm from "@/components/CreateProjectForm";
import Pagination from "@/components/Pagination";
import { getProjects, Project } from "@/lib/api";

const PAGE_SIZE = 5;

export default function ProjectsPage() {
  const router = useRouter();
  const [page, setPage] = useState(1);

  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("access_token") || ""
      : "";

  const role =
    typeof window !== "undefined"
      ? localStorage.getItem("user_role") || ""
      : "";

  useEffect(() => {
    if (!token) {
      router.replace("/login");
    }
  }, [token, router]);

  const { data, error, mutate, isLoading } = useSWR(
    token ? ["projects", token] : null,
    ([, authToken]) => getProjects(authToken)
  );

  const projects: Project[] = data || [];

  const paginatedProjects = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return projects.slice(start, start + PAGE_SIZE);
  }, [projects, page]);

  const totalPages = Math.ceil(projects.length / PAGE_SIZE);

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="p-6">
        <h1 className="mb-4 text-2xl font-bold">Projects</h1>

        {role === "admin" && token && (
          <CreateProjectForm
            token={token}
            onProjectCreated={() => mutate()}
          />
        )}

        {error && (
          <p className="mb-4 text-red-600">Failed to load projects</p>
        )}

        {isLoading && (
          <p className="mb-4 text-gray-600">Loading projects...</p>
        )}

        <div className="grid gap-4">
          {paginatedProjects.map((project) => (
            <div key={project.id} className="rounded bg-white p-4 shadow">
              <h2 className="text-lg font-semibold">{project.name}</h2>
              <p className="mt-1 text-gray-600">
                {project.description || "No description"}
              </p>
            </div>
          ))}

          {!isLoading && projects.length === 0 && !error && (
            <p className="text-gray-600">No projects found.</p>
          )}
        </div>

        {totalPages > 1 && (
          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        )}
      </div>
    </div>
  );
}