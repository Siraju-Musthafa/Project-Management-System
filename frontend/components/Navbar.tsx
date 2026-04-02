"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();

  const role =
    typeof window !== "undefined"
      ? localStorage.getItem("user_role") || ""
      : "";

  const name =
    typeof window !== "undefined"
      ? localStorage.getItem("user_name") || ""
      : "";

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_name");
    router.push("/login");
  };

  return (
    <div className="flex items-center justify-between bg-blue-600 px-6 py-4 text-white">
      <div className="flex items-center gap-5">
        <Link href="/projects" className="font-medium hover:underline">
          Projects
        </Link>

        <Link href="/tasks" className="font-medium hover:underline">
          Tasks
        </Link>

        {role === "admin" && (
          <Link href="/users" className="font-medium hover:underline">
            Users
          </Link>
        )}
      </div>

      <div className="flex items-center gap-4">
        <span className="text-sm">
          {name ? `${name} (${role})` : role}
        </span>
        <button
          onClick={handleLogout}
          className="rounded bg-white px-3 py-1 text-blue-600"
        >
          Logout
        </button>
      </div>
    </div>
  );
}