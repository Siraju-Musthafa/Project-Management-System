"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import useSWR from "swr";
import Navbar from "@/components/Navbar";
import UsersTable from "@/components/UserTable";
import CreateUserForm from "@/components/CreateUserForm";
import Pagination from "@/components/Pagination";
import { getUsers, User } from "@/lib/api";

const PAGE_SIZE = 5;

export default function UsersPage() {
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
      return;
    }

    if (role !== "admin") {
      router.replace("/tasks");
    }
  }, [token, role, router]);

  const { data, error, mutate } = useSWR(
    token && role === "admin" ? ["users", token] : null,
    ([, authToken]) => getUsers(authToken)
  );

  const users: User[] = data || [];

  const paginatedUsers = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return users.slice(start, start + PAGE_SIZE);
  }, [users, page]);

  const totalPages = Math.ceil(users.length / PAGE_SIZE);

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="p-6">
        <h1 className="mb-4 text-2xl font-bold">Users</h1>

        {token && role === "admin" && (
          <CreateUserForm
            token={token}
            onUserCreated={() => mutate()}
          />
        )}

        {error && <p className="mb-4 text-red-600">Failed to load users</p>}

        {!error && <UsersTable users={paginatedUsers} />}

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