"use client";

import { useState } from "react";
import { createUser } from "@/lib/api";

type Props = {
  token: string;
  onUserCreated: () => void;
};

export default function CreateUserForm({ token, onUserCreated }: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("developer");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!name.trim() || !email.trim() || !password.trim()) {
      setError("Name, email and password are required.");
      return;
    }

    setLoading(true);

    try {
      await createUser(token, {
        name,
        email,
        password,
        role,
      });

      setName("");
      setEmail("");
      setPassword("");
      setRole("developer");
      onUserCreated();
    } catch {
      setError("Failed to create user");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-6 rounded bg-white p-4 shadow">
      <h2 className="mb-4 text-xl font-semibold">Create User</h2>

      <form onSubmit={handleSubmit} className="grid gap-3 md:grid-cols-2">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="rounded border px-3 py-2"
        />

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="rounded border px-3 py-2"
        >
          <option value="developer">developer</option>
          <option value="admin">admin</option>
        </select>

        {error && <p className="text-sm text-red-600 md:col-span-2">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="rounded bg-green-600 px-4 py-2 text-white md:col-span-2 disabled:opacity-60"
        >
          {loading ? "Creating..." : "Create User"}
        </button>
      </form>
    </div>
  );
}