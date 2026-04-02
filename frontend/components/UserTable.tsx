import { User } from "@/lib/api";

type Props = {
  users: User[];
};

export default function UsersTable({ users }: Props) {
  return (
    <div className="overflow-x-auto rounded bg-white shadow">
      <table className="min-w-full border-collapse">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-4 py-3 text-left">ID</th>
            <th className="border px-4 py-3 text-left">Name</th>
            <th className="border px-4 py-3 text-left">Email</th>
            <th className="border px-4 py-3 text-left">Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td className="border px-4 py-3">{user.id}</td>
              <td className="border px-4 py-3">{user.name}</td>
              <td className="border px-4 py-3">{user.email}</td>
              <td className="border px-4 py-3">{user.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}