"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      router.push("/projects");
    } else {
      router.push("/login");
    }
  }, [router]);

  return <div className="p-6">Loading...</div>;
}